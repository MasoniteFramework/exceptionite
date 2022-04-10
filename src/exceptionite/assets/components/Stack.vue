<template>
  <div class="bg-white border-transparent shadow-md dark:bg-gray-800 rounded-md flex">
    <div class="shrink-0 rounded-l-md border-r border-gray-300 dark:border-gray-700">
      <div class="border-b border-gray-300 dark:border-gray-700 p-4 flex items-center space-x-2">
        <button
          @click="toggleVendor"
          type="button" class="btn"
          :disabled="vendorsFrameCount == 0"
          :class="{'btn-disabled': vendorsFrameCount === 0}"
          v-tooltip="`Show/Hide vendor frames in stack trace`"
        >
          <SolidSelectorIcon class="-ml-0.5 mr-2 h-4 w-4" />
          {{ showVendors ? "Hide" : "Show" }} Vendor Stacks ({{ vendorsFrameCount }})
        </button>
        <button
          @click="copyStack"
          type="button" class="btn"
          v-tooltip="'Copy Stacktrace'"
        >
          <CheckIcon v-if="copied" class="h-4 w-4 text-green-600" />
          <DuplicateIcon v-else class="h-4 w-4" />
        </button>
        <button
          @click="reverseStack"
          type="button" class="btn"
          v-tooltip="'Toggle Stacktrace order'"
        >
          <SolidSortDescendingIcon v-if="reversed" class="h-4 w-4" />
          <SolidSortAscendingIcon v-else class="h-4 w-4" />
        </button>
      </div>
      <div
        v-for="frame in selectedFrames" :key="frame.relative_file + frame.index"
        class="border-b border-gray-300 dark:border-gray-700 px-2 py-4 text-xs cursor-pointer hover:bg-blue-600 dark:hover:bg-red-600 hover:text-white  dark:hover:text-gray-400"
        :class="[
          isCurrent(frame) ? 'text-white dark:text-gray-200' : frame.is_vendor ? 'text-gray-500 ' : 'text-black dark:text-gray-400 dark:bg-gray-900',
          {'bg-blue-600 dark:bg-red-600': isCurrent(frame)}
        ]"
        @click="selectFrame(frame)"
      >
        <span class="block"
        >{{ frame.relative_file }} : {{ frame.no }}</span>
        <span class="block font-medium">{{ frame.method }}()</span>
      </div>
    </div>
    <div class="self-stretch grow rounded-r-md overflow-x-auto">
      <template v-if="currentFrame">
        <frame :frame="currentFrame" />
        <frame-vars :variables="currentFrame.variables" />
      </template>
      <p v-else class="text-black dark:text-gray-400 p-2 text-center">No frame selected</p>
    </div>
  </div>
</template>

<script>
import Frame from "./Frame.vue"
import FrameVars from "./FrameVars.vue"
import { useStorage, useClipboard } from "@vueuse/core"
import { ref, computed } from "vue"

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
  setup (props) {
    const showVendors = useStorage('exceptionite.showVendors', false)
    const reversed = useStorage('exceptionite.reversed', false)
    const currentFrame = ref(null)
    const stack = ref(props.exception.stacktrace)

    const selectFrame = (frame) => {
      currentFrame.value = frame
    }

    const reverseStack = () => {
      stack.value.reverse()
      reversed.value = !reversed.value
    }
    const { copy, copied } = useClipboard({ copiedDuring: 2000})
    const copyStack = () => {
      copy(JSON.stringify(stack.value))
    }

    const selectedFrames = computed(() => {
      if (!showVendors.value) {
        return stack.value.filter(frame => !frame.is_vendor)
      } else {
        return stack.value
      }
    })

    const vendorsFrameCount = computed(() => stack.value.filter(frame => frame.is_vendor).length)

    const isCurrent = (frame) => {
      if (!currentFrame.value) {
        return false
      }
      return currentFrame.value.index === frame.index
    }
    // set initial reversed state
    if (reversed.value) {
      reverseStack()
      selectFrame(selectedFrames.value[stack.value.length - 1])
    } else {
      selectFrame(selectedFrames.value[0])
    }

    return {
      currentFrame,
      isCurrent,
      showVendors,
      selectFrame,
      stack,
      reversed,
      reverseStack,
      copyStack,
      copied,
      vendorsFrameCount,
      selectedFrames,
    }
  },
  methods: {
    toggleVendor() {
      // if we were showing vendors frame and current is vendor
      // set current as first non vendor
      if (this.showVendors && this.currentFrame?.is_vendor) {
        this.currentFrame = this.stack.filter(frame => !frame.is_vendor)[0]
      }

      // make change
      this.showVendors = !this.showVendors
    }
  },
}
</script>
