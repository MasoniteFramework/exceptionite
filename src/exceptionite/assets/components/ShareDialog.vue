<template>
  <Dialog :open="opened" @close="closeDialog"  class="fixed inset-0 z-30 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen">
      <DialogOverlay class="fixed inset-0 bg-gray-500 opacity-30"  />
      <div class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white dark:bg-gray-800 dark:text-gray-300 shadow-xl rounded-2xl relative">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            @click="closeDialog"
            type="button"
            class="navbar-link group"
          >
            <XIcon class="navbar-link-icon-only" />
          </button>
        </div>
        <DialogTitle class="mb-4 font-medium">Share Error</DialogTitle>
        <DialogDescription class="text-sm">
          You can choose which elements of the exception you want to copy.
        </DialogDescription>

        <share-selector class="my-4" v-model="shareOptions" />

        <div class="text-right">
          <button class="btn mr-2" @click="copyRaw">
            <CheckIcon v-if="copied && copyType == 'raw'" class="h-4 w-4 text-green-600" />
            <DuplicateIcon v-else class="h-4 w-4" />
            <span class="ml-2">Copy Raw</span>
          </button>
          <button class="btn mr-2" @click="copyMarkdown">
            <CheckIcon v-if="copied && copyType == 'markdown'" class="h-4 w-4 text-green-600" />
            <DuplicateIcon v-else class="h-4 w-4" />
            <span class="ml-2">Copy as Markdown</span>
          </button>
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
import { computed, ref } from "vue"
import ShareSelector from "./ShareSelector.vue"
import { useClipboard } from "@vueuse/core"

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
    const { copy, copied } = useClipboard({ copiedDuring: 2000})
    const copyType = ref()
    return {
      opened,
      closeDialog,
      copy,
      copied,
      copyType,
    }
  },
  inject: ["exception", "context", "shareOptions"],
  methods: {
    copyRaw () {
      this.copyType = "raw"
      let text = ""
      if (this.shareOptions.exception.show) {
        text += `* Exception: ${this.exception.type} - ${this.exception.message}\n\n`
      }
      if (this.shareOptions.stacktrace.show) {
        let stacktrace = []
        if (this.shareOptions.stacktrace.first_frame) {
          stacktrace.push(this.exception.stacktrace[0])
        } else {
          stacktrace = this.exception.stacktrace
        }
        const stack = stacktrace.map(frame => {
          return {content: Object.values(frame.content).map(line => "\t" + line).join("\n"), title: `${frame.file}: L${frame.no}`}
        })
        text += `* Stack trace:\n\n`
        stack.forEach(frame => {
          text += `-> ${frame.title}:\n\n${frame.content}\n\n`
        })
        text += "\n"
      }
      if (this.shareOptions.context.show) {
        text += `* Context:\n\n`
        this.context.forEach(section => {
          if (this.shareOptions.context[section.name]){
            text += `\t* ${section.name}:\n\n`
            Object.entries(section.data).forEach(entry => {
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
      this.copyType = "markdown"
      let text = ""
      if (this.shareOptions.exception.show) {
        text += `## Exception\n\`${this.exception.type}\` - \`${this.exception.message}\`\n\n`
      }
      if (this.shareOptions.stacktrace.show) {
        let stacktrace = []
        if (this.shareOptions.stacktrace.first_frame) {
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
      if (this.shareOptions.context.show) {
        text += `## Context\n`
        this.context.forEach(section => {
          if (this.shareOptions.context[section.name]){
            text += `\n### ${section.name}\n`
            Object.entries(section.data).forEach(entry => {
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
