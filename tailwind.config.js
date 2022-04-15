module.exports = {
  content: [
    "src/exceptionite/assets/**/*.vue",
    "src/exceptionite/assets/**/*.js",
    "src/exceptionite/templates/exception.html"
  ],
  safelist: [
    {
      pattern: /bg-(gray|red|yellow|green|blue|indigo|purple|pink)-(100|800)/,
    },
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
}
