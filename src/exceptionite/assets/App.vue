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
        <span class="text-black dark:text-gray-300 font-medium truncate"> {{ exception.message }}</span>
      </div>
    </div>

    <!-- page content -->
    <div class="container mx-auto py-4 lg:p-4">
      <sponsor />
      <div ref="exceptioniteBlock">
        <exception :exception="exception" />
      </div>

      <first-solution v-if="firstSolution" :solution="firstSolution" class="mt-4" />
      <no-solution v-else-if="!firstSolution && showSolutionRequest" class="mt-4" :link="requestLink" @click="showSolutionRequest = false" />

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
      <p class="text-gray-600 dark:text-gray-400 text-xs text-center">v{{ config.version }}</p>
    </div>
    <share-dialog v-model="sharing" />
    <base-action-dialog v-if="selectedAction" :action="selectedAction" @close="selectedAction = null"  />
  </div>
</template>

<script>
import { ref, computed, provide } from 'vue'
import { useElementVisibility, useStorage } from '@vueuse/core'
import Navbar from "@/components/Navbar.vue"
import Sponsor from "@/components/Sponsor.vue"
import Exception from '@/components/Exception.vue'
import Stack from '@/components/Stack.vue'
import ContextMenu from '@/components/ContextMenu.vue'
import FirstSolution from '@/components/FirstSolution.vue'
import NoSolution from '@/components/NoSolution.vue'
import Pulse from '@/components/Pulse.vue'
import ShareDialog from '@/components/ShareDialog.vue'
import BaseActionDialog from '@/components/BaseActionDialog.vue'

export default {
  components: {
    Exception,
    Stack,
    Sponsor,
    ContextMenu,
    Navbar,
    ShareDialog,
    BaseActionDialog,
    Pulse,
    FirstSolution,
    NoSolution,
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
    const currentTab = ref(props.tabs.find(tab => tab.id == defaultTabId.value) || props.tabs[0].id)
    const selectTab = (tab) =>{
      currentTab.value = tab
      defaultTabId.value = tab.id
    }
    const sharing = ref(false)
    const selectedAction = ref(null)

    // solutions enabled ?
    const solutionsTab = props.tabs.find(tab => tab.id == "solutions")
    const possibleSolutions = solutionsTab !== undefined && solutionsTab.blocks.find(block => block.id === "possible_solutions")
    const requestLink = ref(possibleSolutions?.data?.request_link || "#")
    const firstSolution = computed(() => {
      if (possibleSolutions !== undefined) {
        return possibleSolutions.data.first
      }
      return false
    })
    const showSolutionRequest = ref(true)

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
        // try setting sensible default options
        shareOptions.value.context[item.name] = !["packages", "git", "config"].includes(item.id)
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
      showSolutionRequest,
      requestLink,
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
