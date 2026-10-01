import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  "#f0f4ff",
          100: "#e0e9ff",
          200: "#c7d6ff",
          300: "#a4b8fd",
          400: "#7e92fa",
          500: "#5a6cf4",
          600: "#3d4de8",
          700: "#2f3ccd",
          800: "#2934a5",
          900: "#272f83",
          950: "#181c4d",
        },
        neutral: {
          50:  "#f8f9fb",
          100: "#f1f3f7",
          200: "#e4e7ef",
          300: "#cdd2df",
          400: "#9aa3b8",
          500: "#697488",
          600: "#4e5a70",
          700: "#3b4560",
          800: "#27304f",
          900: "#161e38",
          950: "#0c1020",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        DEFAULT: "0.5rem",
      },
      boxShadow: {
        card: "0 1px 3px 0 rgb(0 0 0 / 0.08), 0 1px 2px -1px rgb(0 0 0 / 0.06)",
        "card-hover": "0 4px 12px 0 rgb(0 0 0 / 0.1), 0 2px 4px -1px rgb(0 0 0 / 0.06)",
      },
    },
  },
  plugins: [],
};

export default config;
