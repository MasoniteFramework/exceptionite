<template>
  <div class="bg-white border-transparent shadow-md dark:bg-gray-800 rounded-md flex">
    <div class="shrink-0 rounded-l-md border-r border-gray-300 dark:border-gray-700">
      <div class="border-b border-gray-300 dark:border-gray-700 p-4 flex items-center space-x-2">
        <button
          @click="toggleVendor"
          type="button" class="stack-button"
        >
          <SolidSelectorIcon class="-ml-0.5 mr-2 h-4 w-4" />
          {{ showVendors ? "Hide" : "Show" }} Vendor ({{ vendorsFrameCount }})
          <span class="tooltip">{{ showVendors ? "Hide" : "Show" }} vendor frames in stack trace</span>
        </button>
        <button
          @click="copyStack"
          type="button" class="stack-button"
        >
          <DuplicateIcon class="h-4 w-4" />
          <span class="tooltip">Copy stacktrace</span>
        </button>
        <button
          @click="reverseStack"
          type="button" class="stack-button"
        >
          <SolidSortAscendingIcon v-if="inversed" class="h-4 w-4" />
          <SolidSortDescendingIcon v-else class="h-4 w-4" />
          <span class="tooltip">Reverse stacktrace</span>
        </button>
      </div>
      <div
        v-for="frame in selectedFrames" :key="frame.relative_file"
        class="border-b border-gray-300 dark:border-gray-700 px-2 py-4 text-xs cursor-pointer hover:bg-red-500 hover:text-white"
        :class="[
          currentFrame.id == frame.id ? 'text-white' : frame.is_vendor ? 'text-gray-500 ' : 'text-black dark:text-white dark:bg-gray-900',
          {'bg-red-500': currentFrame.id == frame.id}
        ]"
        @click="selectFrame(frame)"
      >
        <span class="block"
        >{{ frame.relative_file }} : {{ frame.no }}</span>
        <span class="block font-medium">{{ frame.method }}()</span>
      </div>
    </div>
    <div class="self-stretch grow rounded-r-md">
      <frame :frame="currentFrame" />
      <frame-vars :variables="currentFrame.variables" />
    </div>
  </div>
</template>

<script>
import Frame from "./Frame.vue"
import FrameVars from "./FrameVars.vue"
import { useStorage } from "@vueuse/core"
import { provide, ref, inject } from "vue"

export default {
  name: "Stack",
  components: {
    Frame,
    FrameVars,
  },
  props: {
    exception: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      inversed: false,
    }
  },
  setup (props) {
    const showVendors = useStorage('exceptionite.showVendors', false)
    const currentFrame = ref(null)
    const marker = "site-packages/"
    const localMarker = "masonite/src/"
    const selectFrame = (frame) => {
      currentFrame.value = frame
    }
    const config = inject("config")
    const stack = ref(props.exception.stacktrace.map((frame, index) => {
      let relativePath = frame.file.replace(`${config.absolute_path}/`, '')
      const isVendor = !frame.file.startsWith(config.absolute_path)
      if (isVendor) {
        const index = relativePath.indexOf(marker)
        if (index !== -1) {
          relativePath = "~" + relativePath.slice(index + marker.length, )
        }
        else {
          // cut local Masonite installations too
          const index = relativePath.indexOf(localMarker)
          if (index !== -1) {
            relativePath = "~" + relativePath.slice(index + localMarker.length, )
          }
        }
      }
      relativePath = relativePath.replace(/\.[^.$]+$/, '')
      return {
        ...frame,
        id: relativePath + index,
        relative_file: relativePath,
        is_vendor: isVendor
      }
    }))

    provide("stack", stack)

    selectFrame(stack.value[0])

    return {
      stack,
      currentFrame,
      showVendors,
      selectFrame,
      config,
    }
  },
  computed: {
    selectedFrames () {
      if (!this.showVendors) {
        return this.stack.filter(frame => !frame.is_vendor)
      } else {
        return this.stack
      }
    },
    vendorsFrameCount() {
      return this.stack.filter(frame => frame.is_vendor).length
    },
  },
  methods: {
    copyStack () {
      navigator.clipboard.writeText(this.stack)
    },
    reverseStack () {
      this.stack.reverse()
      this.inversed = !this.inversed
    },
    toggleVendor() {
      this.showVendors = !this.showVendors
      if (!this.showVendors) {
        this.selectFrame(this.selectedFrames[0])
      }
    }
  },
  // created () {
  //   //transform stack trace
  //   this.stack = this.exception.stacktrace.map((frame, index) => {
  //     let relativePath = frame.file.replace(`${this.config.absolute_path}/`, '')
  //     const isVendor = !frame.file.startsWith(this.config.absolute_path)
  //     if (isVendor) {
  //       const index = relativePath.indexOf(this.marker)
  //       if (index !== -1) {
  //         relativePath = "~" + relativePath.slice(index + this.marker.length, )
  //       }
  //       else {
  //         // cut local Masonite installations too
  //         const index = relativePath.indexOf(this.localMarker)
  //         if (index !== -1) {
  //           relativePath = "~" + relativePath.slice(index + this.localMarker.length, )
  //         }
  //       }
  //     }
  //     relativePath = relativePath.replace(/\.[^.$]+$/, '')
  //     return {
  //       ...frame,
  //       id: relativePath + index,
  //       relative_file: relativePath,
  //       is_vendor: isVendor
  //     }
  //   })
  //   provide("stack", this.stack)
  //   this.selectFrame(this.stack[0])
  // }
}
</script>
