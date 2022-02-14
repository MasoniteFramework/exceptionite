<template>
  <div class="bg-gray-300 dark:bg-gray-700 w-full h-full">
    <navbar
      :tabs="tabs"
      @open="selectTab"
      @share="sharing=true"
      @action="openAction"
      @search="search"
    />
    <!-- exception reminder when exception block is hidden  -->
    <div
      v-if="!exceptioniteShown"
      class="w-full sticky shadow-md z-30 top-14 bg-white dark:bg-gray-900 h-10 flex"
    >
      <div class="container mx-auto px-4 flex items-center self-stretch text-sm">
        <span class="text-red-600 font-bold">{{ exception.type }}</span>
        <span class="text-black dark:text-gray-400 font-medium">&nbsp;-&nbsp;</span>
        <span class="text-black dark:text-gray-300 font-medium"> {{ exception.message }}</span>
      </div>
    </div>

    <!-- page content -->
    <div class="container mx-auto lg:p-4">
      <div ref="exceptioniteBlock">
        <exception :exception="exception" />
      </div>

      <first-solution v-if="firstSolution" :solution="firstSolution" class="mt-4" />

      <stack id="stack" class="mt-4 mb-10" :exception="exception" />

      <!-- All integrations -->
      <div class="grid grid-cols-4 gap-4" id="exceptionite-tabs">
        <div
          v-if="contextTab"
          class="col-span-1"
        >
          <!-- menu -->
          <context-menu :menu="contextTab.blocks" @browse="toContextMenu"/>
        </div>
        <div :class="contextTab ? 'col-span-3' : 'col-span-4'">
          <!-- tabs -->
          <nav class="flex space-x-4 mb-4">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="[
                currentTab.id === tab.id ? 'bg-white dark:bg-gray-800 dark:text-gray-300 text-blue-500' : 'text-gray-600 dark:text-gray-400 hover:text-blue-500 hover:bg-white dark:hover:bg-gray-800 dark:hover:text-gray-300',
                'px-3 py-2 font-medium text-sm rounded-md relative flex items-center'
              ]"
              @click="selectTab(tab)"
            >
              <pulse v-if="tab.advertise_content && tab.has_content" />
              <component v-if="tab.icon" :is="tab.icon" class="h-4 w-4 mr-1" />
              <span>{{ tab.name }}</span>
            </button>
          </nav>
          <keep-alive v-if="currentTab">
            <component :is="currentTab.component" :data="currentTab" />
          </keep-alive>
        </div>

      </div>
    </div>
    <share-dialog v-model="sharing" />
    <base-action-dialog v-if="selectedAction" :action="selectedAction" @close="selectedAction = null"  />
  </div>
</template>

<script>
import Navbar from "./Navbar.vue"
import Exception from './Exception.vue'
import Stack from './Stack.vue'
import ContextMenu from './ContextMenu.vue'
import FirstSolution from './FirstSolution.vue'
import Pulse from './Pulse.vue'
import ShareDialog from './ShareDialog.vue'
import BaseActionDialog from './BaseActionDialog.vue'
import { ref, computed, provide } from 'vue'
import { useElementVisibility, useStorage } from '@vueuse/core'

export default {
  components: {
    Exception,
    Stack,
    ContextMenu,
    Navbar,
    ShareDialog,
    BaseActionDialog,
    Pulse,
    FirstSolution,
  },
  props: {
    config: { required: true },
    exception: { required: true },
    tabs: { required: true },
    actions: { required: true },
  },
  provide() {
    return {
      config: this.config,
      tabs: this.tabs,
      exception: this.exception,
      actions: this.actions,
    }
  },
  setup (props) {
    const exceptioniteBlock = ref(null)
    const exceptioniteShown = useElementVisibility(exceptioniteBlock)
    const contextTab = computed(() => props.tabs.find(tab => tab.id == "context"))
    const context = contextTab.value?.blocks
    provide("context", context)
    // open "context" tab by default and save it in local storage
    const defaultTabId = useStorage('exceptionite.tab', contextTab.value ? contextTab.value.id : props.tabs[0].id)
    const currentTab = ref(props.tabs.find(tab => tab.id == defaultTabId.value))
    const selectTab = (tab) =>{
      currentTab.value = tab
      defaultTabId.value = tab.id
    }
    const sharing = ref(false)
    const selectedAction = ref(null)

    // solutions enabled ?
    const firstSolution = computed(() => {
      const solutionsTab = props.tabs.find(tab => tab.id == "solutions")
      if (solutionsTab !== undefined) {
        const possibleSolutions = solutionsTab.blocks.find(block => block.id === "possible_solutions")
        if (possibleSolutions !== undefined) {
          return possibleSolutions.data.first
        }
      }
      return false
    })

    // prepare default sharing settings
    const shareOptions = ref({
      exception: {
        show: true
      },
      stacktrace: {
        show: true,
        first_frame: true
      },
      context: {
        show: true
      }
    })
    if (context) {
      context.forEach(item => {
        shareOptions.value.context[item.name] = true
      })
    }
    provide("shareOptions", shareOptions.value)

    return {
      exceptioniteBlock,
      exceptioniteShown,
      // tab handling
      contextTab,
      defaultTabId,
      selectTab,
      currentTab,
      sharing,
      // action handling
      selectedAction,
      firstSolution,
    }
  },
  methods: {
    openAction (action) {
      this.selectedAction = action
    },
    search () {
      const url = `${this.config.options.search_url}${encodeURIComponent(this.exception.type + " " +this.exception.message)}`
      window.open(url, "_blank")
    },
    toContextMenu(id) {
      // ensure context tab is opened
      this.selectTab(this.contextTab)
      this.$nextTick(function() {
        // go to context section
        this.$root.goToElement(id)
      })
    }
  }
}
</script>
