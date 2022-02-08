<template>
  <div class="sticky top-0 bg-white dark:bg-gray-800 py-2 h-14 z-40 shadow-md">
    <div class="flex justify-between items-center container px-4 mx-auto">
      <div class="flex justify-start items-center space-x-2">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="showTab(tab)"
          class="navbar-link relative group"
        >
          <component v-if="tab.icon" :is="tab.icon" class="navbar-link-icon mr-1" />
          <pulse v-if="tab.advertise_content && tab.has_content" />
          <span class="hidden md:inline">{{ tab.name }}</span>
        </button>
      </div>
      <div class="flex justify-end items-center space-x-2">
        <!-- <button
          @click="$emit('support')"
          class="navbar-link has-tooltip"
        >
          <SupportIcon class="h-5 w-5" />
          <span class="tooltip">Get support</span>
        </button> -->
        <!-- Actions -->
        <Menu as="div" class="relative inline-block text-left">
          <MenuButton as="button" class="navbar-link has-tooltip group">
            <PlayIcon class="navbar-link-icon-only" />
            <span class="tooltip">Run actions</span>
          </MenuButton>
          <MenuItems
            class="absolute right-0 w-72 mt-4 origin-top-right bg-white px-1 py-1 dark:bg-gray-800 divide-y divide-gray-100 dark:divide-gray-400 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
          >
            <MenuItem
              as="button"
              v-for="action in actions"
              :key="action.id"
              class="group flex items-center w-full px-2 py-2 text-sm text-gray-900 dark:text-gray-300 hover:bg-purple-100 dark:hover:bg-gray-700"
              @click="openActionDialog(action)"
            >
              <component v-if="action.icon" class="navbar-link-icon mr-1" :is="action.icon" />
              {{ action.name }}
            </MenuItem>
          </MenuItems>
        </Menu>

        <button
          @click="$emit('share')"
          class="navbar-link has-tooltip group"
        >
          <ShareIcon class="navbar-link-icon-only" />
          <span class="tooltip">Share error</span>
        </button>
        <button
          @click="$emit('search')"
          class="navbar-link has-tooltip group"
        >
          <SearchIcon class="navbar-link-icon-only" />
          <span class="tooltip">Search on the web</span>
        </button>
        <a
          v-if="config.links.doc"
          :href="config.links.doc"
          target="_blank"
          class="navbar-link has-tooltip group"
        >
          <DocumentTextIcon class="navbar-link-icon-only" />
          <span class="tooltip">Open doc</span>
        </a>

        <a
          v-if="config.links.repo"
          :href="config.links.repo"
          target="_blank"
          class="navbar-link has-tooltip group"
        >
          <svg class="navbar-link-icon-only" viewBox="0 0 24 24">
            <path fill="currentColor" d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2Z"></path>
          </svg>
          <span class="tooltip">Open repository</span>
        </a>
        <button
          @click="$root.toggleTheme()"
          class="navbar-link has-tooltip group"
        >
          <SunIcon class="navbar-link-icon-only group-hover:text-yellow-500" v-if="$root.theme === 'dark'"/>
          <MoonIcon class="navbar-link-icon-only group-hover:text-red-600" v-else />
          <span class="tooltip">Toggle Light/Dark theme</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { ref } from "vue"
import Pulse from "./Pulse.vue"

export default {
  name: "Navbar",
  components: {
    Menu,
    MenuButton,
    MenuItems,
    MenuItem,
    Pulse,
  },
  emits: ["open", "update:modelValue", "share", "action"],
  inject: ["tabs", "config", "actions"],
  setup(props, context) {
    const share = ref({
      exception: true,
      stacktrace: true,
      context: true,
    })
    const selected = ref("stack")
    const select = (item) => {
      selected.value = item
    }
    return {
      share,
      selected,
      select,
    }
  },
  methods: {
    showTab (tab) {
      this.$emit("open", tab)
      this.select(`tab-${tab.id}`)
      this.$root.goToElement("exceptionite-tabs")
    },
    openActionDialog (action) {
      this.$emit("action", action)
    }
  }
}
</script>
