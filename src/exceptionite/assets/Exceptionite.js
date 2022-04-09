import { createApp, h } from "vue"
import App from "./App.vue"
import Badge from "./components/Badge.vue"
import AppButton from "./components/AppButton.vue"
import KeyValList from "./components/blocks/KeyValList.vue"
import KeyValItem from "./components/blocks/KeyValItem.vue"
import KeyValBlock from "./components/blocks/KeyValBlock.vue"
import StackOverflowBlock from "./components/blocks/StackOverflowBlock.vue"
import PossibleSolutionsBlock from "./components/blocks/PossibleSolutionsBlock.vue"
import PackagesUpdatesBlock from "./components/blocks/PackagesUpdatesBlock.vue"
import KeyValBlockWithSections from "./components/blocks/KeyValBlockWithSections.vue"
import CopyButton from "./components/CopyButton.vue"
import hljs from 'highlight.js'
import axios from "axios"
// tooltips
import tippy from "tippy.js"
import 'tippy.js/dist/tippy.css';

// tabs
import BaseTab from "./components/tabs/BaseTab.vue"
import DumpsTab from "./components/tabs/DumpsTab.vue"
// icons
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
    this.app.component('KeyValItem', KeyValItem)
    this.app.component('KeyValList', KeyValList)
    this.app.component('KeyValBlock', KeyValBlock)
    this.app.component('KeyValBlockWithSections', KeyValBlockWithSections)
    this.app.component('StackOverflowBlock', StackOverflowBlock)
    this.app.component('PossibleSolutionsBlock', PossibleSolutionsBlock)
    this.app.component('PackagesUpdatesBlock', PackagesUpdatesBlock)
    this.app.component('CopyButton', CopyButton)
  }
  registerBuiltinTabs() {
    this.app.component('BaseTab', BaseTab)
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
