<template>
  <Dialog :open="opened" @close="closeDialog"  class="fixed inset-0 z-30 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen">
      <DialogOverlay class="fixed inset-0 bg-gray-500 opacity-30"  />
      <div class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white dark:bg-gray-800 dark:text-gray-300 shadow-xl rounded-2xl relative">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            @click="closeDialog"
            type="button"
            class="navbar-link">
            <XIcon class="navbar-link-icon" />
          </button>
        </div>
        <DialogTitle class="mb-4">Share Error</DialogTitle>
        <DialogDescription class="text-sm">
          You can choose what do you want to share.
        </DialogDescription>

        <share-selector class="my-4" v-model="shareOptions" />

        <div class="text-right">
          <button class="btn mr-2" @click="copyRaw">Copy Raw</button>
          <button class="btn mr-2" @click="copyMarkdown">Copy To MarkDown</button>
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script>
import {
  Dialog,
  DialogOverlay,
  DialogTitle,
  DialogDescription,
} from "@headlessui/vue"
import { ref, computed } from "vue"
import ShareSelector from "./ShareSelector.vue"
export default {
  name: "ShareDialog",
  components: {
    Dialog, DialogOverlay, DialogTitle, DialogDescription, ShareSelector
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  setup (props, context) {
    const opened = computed({
      get () {
        return props.modelValue
      },
      set (value) {
        context.emit("update:modelValue", value)
      },
    })
    const closeDialog = () => {
      opened.value = false
    }
    // const shareOptions = inject("shareOptions")
    const copied = ref(false)
    const timeout = ref(null)
    return {
      opened,
      closeDialog,
      // shareOptions,
      copied,
      timeout,
    }
  },
  inject: ["exception", "context", "shareOptions"],
  methods: {
    copy (text) {
      if (this.timeout) {
        window.clearTimeout(this.timeout);
      }
      navigator.clipboard.writeText(text)
      this.copied = true;
      this.timeout = window.setTimeout(() => (this.copied = false), 2000);
    },
    copyRaw () {
      let text = ""
      if (this.shareOptions.exception) {
        text += `* Exception: ${this.exception.type} - ${this.exception.message}\n\n`
      }
      if (this.shareOptions.stacktrace) {
        const stack = this.exception.stacktrace.map(frame => {
          return {content: Object.values(frame.content).map(line => "\t" + line).join("\n"), title: `${frame.file}: L${frame.no}`}
        })
        text += `* Stack trace:\n\n`
        stack.forEach(frame => {
          text += `-> ${frame.title}:\n\n${frame.content}\n\n`
        })
        text += "\n"
      }
      if (this.shareOptions.context) {
        text += `* Context:\n\n`
        this.context.forEach((value, index) => {
          if (this.contextSelection[index]){
            text += `\t* ${value.name}:\n\n`
            Object.entries(value.data).forEach(entry => {
              const [key, value] = entry
              text += `\t\t${key}: ${JSON.stringify(value)}\n`
            })
            text += "\n"
          }
        })
        text += "\n\n\n"
      }
      this.copy(text)
    },
    copyMarkdown () {
      let text = ""
      if (this.shareOptions.exception) {
        text += `## Exception\n\`${this.exception.type}\` - \`${this.exception.message}\`\n\n`
      }
      if (this.shareOptions.stacktrace) {
        let stacktrace = []
        if (this.firstFrame) {
          stacktrace.push(this.exception.stacktrace[0])
        } else {
          stacktrace = this.exception.stacktrace
        }
        const stack = stacktrace.map(frame => {
          return {content: Object.values(frame.content).map(line => "\t" + line).join("\n"), title: `${frame.file}: L${frame.no}`}
        })
        text += `## Stack trace\n`
        stack.forEach(frame => {
          text += `-> ${frame.title}:\n\n\`\`\`python\n${frame.content}\n\`\`\`\n\n`
        })
        text += "\n"
      }
      if (this.shareOptions.context) {
        text += `## Context\n`
        this.context.forEach((value, index) => {
          if (this.contextSelection[index]){
            text += `\n### ${value.name}\n`
            Object.entries(value.data).forEach(entry => {
              const [key, value] = entry
              text += `\`${key}\`: \`${JSON.stringify(value)}\` \n`
            })
          }
        })

      }
      this.copy(text)
    }
  }
}
</script>
