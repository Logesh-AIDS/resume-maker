"""
Auth routes: signup, login, logout, refresh, /me
"""
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from src.api.deps import CurrentUser, get_auth_service
from src.core.config import get_settings
from src.core.exceptions import ConflictError, UnauthorizedError
from src.schemas.auth import (
    AuthResponse,
    LoginRequest,
    MessageResponse,
    RefreshResponse,
    SignupRequest,
    UserOut,
)
from src.services.auth_service import AuthService
from src.core.security import create_refresh_token

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["auth"])


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Set the httpOnly refresh token cookie."""
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.is_production,   # https-only in prod
        samesite="lax",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path="/api/v1/auth",             # scoped to auth endpoints only
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth",
    )


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new account",
)
async def signup(
    body: SignupRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    try:
        result = await auth_service.signup(body.email, body.password)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=exc.message) from exc

    refresh_token = create_refresh_token(str(result.user.id))
    _set_refresh_cookie(response, refresh_token)
    return result


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Log in with email and password",
)
async def login(
    body: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    try:
        result = await auth_service.login(body.email, body.password)
    except UnauthorizedError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc

    refresh_token = create_refresh_token(str(result.user.id))
    _set_refresh_cookie(response, refresh_token)
    return result


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    summary="Exchange refresh token for new access token",
)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    auth_service: AuthService = Depends(get_auth_service),
) -> RefreshResponse:
    if not refresh_token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided.",
        )
    try:
        new_access, user = await auth_service.refresh(refresh_token)
    except UnauthorizedError as exc:
        _clear_refresh_cookie(response)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=exc.message) from exc

    # Rotate refresh token on every use (security best practice)
    new_refresh = create_refresh_token(str(user.id))
    _set_refresh_cookie(response, new_refresh)

    return RefreshResponse(access_token=new_access)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Log out and clear session",
)
async def logout(response: Response) -> MessageResponse:
    _clear_refresh_cookie(response)
    return MessageResponse(message="Logged out successfully.")


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current authenticated user",
)
async def me(current_user: CurrentUser) -> UserOut:
    return UserOut.model_validate(current_user)
