<template>
  <Dialog :open="opened" @close="closeDialog"  class="fixed inset-0 z-30 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen">
      <DialogOverlay class="fixed inset-0 bg-gray-500 opacity-30"  />
      <div class="inline-block w-full max-w-4xl p-6 my-8 overflow-hidden align-middle transition-all transform bg-white dark:bg-gray-800 dark:text-gray-300 shadow-xl rounded-2xl relative">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            @click="closeDialog"
            type="button"
            class="navbar-link">
            <XIcon class="navbar-link-icon" />
          </button>
        </div>
        <DialogTitle class="mb-4">Get support</DialogTitle>

        <div class="flex items-center">
          <button
            class="stack-button mr-2"
            v-for="action in actions" :key="action.id"
            @click="run(action)"
          >
            {{ action.name }}
          </button>
          <p v-if="running">Running ...</p>
          <p v-else-if="message">{{ message }}</p>
          <!-- <button class="stack-button mr-2" @click="selectSupport">Open an issue</button>
          <button class="stack-button mr-2" @click="selectSupport('MasoniteSupport')">Get Masonite support</button>
          <button class="stack-button mr-2" @click="selectSupport">Post on StackOverflow</button> -->
        </div>
        <!-- <component :is="supportComponent" /> -->
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
export default {
  name: "SupportDialog",
  components: {
    Dialog, DialogOverlay, DialogTitle, DialogDescription,
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  inject: ["actions"],
  setup (props, ctx) {
    const opened = computed({
      get () {
        return props.modelValue
      },
      set (value) {
        ctx.emit("update:modelValue", value)
      },
    })
    const closeDialog = () => {
      opened.value = false
    }
    const message = ref("")
    const running = ref(false)
    return {
      opened,
      closeDialog,
      message,
      running,
    }
  },
  methods: {
    run (action) {
      this.axios.post("/_exceptionite/actions/", {"action_id": action.id}).then(response => {
        this.message = response.data.message
      }).catch(error => {
        console.error(error)
        this.message = error.toString()
      })
    }
  }
}
</script>
