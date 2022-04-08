let mix = require('laravel-mix')
const path = require("path")

mix
.setPublicPath("src/exceptionite/templates")
.js('src/exceptionite/assets/app.js', 'exceptionite.js').vue()
.postCss("src/exceptionite/assets/app.css", "exceptionite.css",
  [require("tailwindcss"),]
)

mix.alias({
  "@": path.resolve("src/exceptionite/assets"),
})

mix.disableSuccessNotifications()