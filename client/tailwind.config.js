/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      keyframes: {
        popOut: {
          "0%": { opacity: "0" },
          "100%": { opacity: "0.5" },
        },
      },
      animation: {
        popOut: "popOut 0.5s ease-in-out",
      },
    },
  },
  plugins: [],
};
