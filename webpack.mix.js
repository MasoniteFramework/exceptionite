let mix = require('laravel-mix');

mix
.setPublicPath("src/exceptionite/templates")
.js('src/exceptionite/assets/app.js', 'pyexceptions.js').vue()
.postCss("src/exceptionite/assets/app.css", "pyexceptions.css",
  [require("tailwindcss"),]
)

mix.disableSuccessNotifications()