import { createApp, h } from "vue"
import hljs from 'highlight.js'
import axios from "axios"
import App from "./App.vue"

// UI
import Badge from "./components/Badge.vue"
import AppButton from "@/components/AppButton.vue"
import CopyButton from "./components/CopyButton.vue"
import tippy from "tippy.js"
import 'tippy.js/dist/tippy.css';

// Blocks
import {
  BasicBlock,
  PackagesUpdatesBlock,
  PossibleSolutionsBlock,
  StackOverflowBlock
} from "@/components/blocks"

// Tabs
import { BasicTab, DumpsTab } from "@/components/tabs"

// Icons
import * as outlineIcons from "@heroicons/vue/outline"
import * as solidIcons from "@heroicons/vue/solid"


export default class Exceptionite {
  constructor(data) {
    this.app = null;
    this.data = data;
    this.tabCallbacks = [];
  }
  registerIcons() {
    Object.entries(outlineIcons).forEach(entry => {
      this.app.component(entry[0], outlineIcons[entry[0]])
    })
     Object.entries(solidIcons).forEach(entry => {
      this.app.component(`Solid${entry[0]}`, solidIcons[entry[0]])
    })
  }
  registerSharedComponents() {
    this.app.component('AppButton', AppButton)
    this.app.component('Badge', Badge)
    this.app.component('CopyButton', CopyButton)
    this.app.component('BasicBlock', BasicBlock)
    this.app.component('StackOverflowBlock', StackOverflowBlock)
    this.app.component('PossibleSolutionsBlock', PossibleSolutionsBlock)
    this.app.component('PackagesUpdatesBlock', PackagesUpdatesBlock)
  }
  registerBuiltinTabs() {
    this.app.component('BasicTab', BasicTab)
    this.app.component('DumpsTab', DumpsTab)
  }
  registerCustomTabs() {
    this.tabCallbacks.forEach(callback => callback(this.app, this.data));
    this.tabCallbacks = [];
  }
  registerTab(callback) {
    this.tabCallbacks.push(callback);
  }

  start() {
    const app = createApp({
      data: () => {
        return {
          ...this.data,
          theme: null,
        }
      },
      methods: {
        copy (text) {
          console.log(text)
        },
        goToElement (id) {
          const offset = 56 + 40 + + 20 // navbar height + exception subnavbar height+ padding
          window.scrollTo(0, 0)
          var rect = document.getElementById(id).getBoundingClientRect()
          window.scrollTo(rect.left , rect.top - offset)
        },
        highlightCode (language, code) {
          const result = hljs.highlight(code, {language: language})
          return result.value || '&nbsp;'
        },
        toggleTheme () {
          if (this.theme === "dark") {
            this.setTheme("light")
          } else {
            this.setTheme("dark")
          }
        },
        setTheme(theme) {
          if (theme === "dark") {
            document.documentElement.classList.add('dark')
          } else {
            document.documentElement.classList.remove('dark')
          }
          this.theme = theme
          localStorage["exceptionite.theme"] = this.theme
        }
      },
      mounted () {
        if (
          localStorage["exceptionite.theme"] === 'dark' || (!('exceptionite.theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
        ) {
          this.setTheme("dark")
        } else {
          this.setTheme("light")
        }
      },
      render: () => {
        return h(App, this.data)
      },
    })

    app.config.globalProperties.axios = axios

    app.directive('tooltip', {
      mounted(el, binding) {
        tippy(el, {
          content: binding.value
        })
      }
    })

    window.app = app
    this.app = app

    this.registerIcons()
    this.registerSharedComponents()
    this.registerBuiltinTabs()
    this.registerCustomTabs()

    app.mount('#app')
  }
}
