<template>
  <Dialog :open="opened" @close="closeDialog"  class="fixed inset-0 z-30 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen">
      <DialogOverlay class="fixed inset-0 bg-gray-500 opacity-30"  />
      <div class="inline-block w-full max-w-4xl p-6 my-8 overflow-hidden align-middle transition-all transform bg-white dark:bg-gray-800 dark:text-gray-300 shadow-xl rounded-2xl relative">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            @click="closeDialog"
            type="button"
            class="navbar-link"
          >
            <XIcon class="navbar-link-icon" />
          </button>
        </div>
        <DialogTitle class="mb-4 text-indigo-600 font-medium">{{ action.name }}</DialogTitle>
        <component
          :is="action.component"
          @run="run"
          :success="success"
          :data="data"
          :running="running"
          @close="closeDialog"
        />
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
import { ref } from "vue"
export default {
  name: "BaseActionDialog",
  components: {
    Dialog, DialogOverlay, DialogTitle, DialogDescription,
  },
  props: {
    action: {
      type: [Object, null],
      required:true
    },
  },
  emits: ["close"],
  setup (props, ctx) {
    const closeDialog = () => {
      opened.value = false
    }
    const opened = ref(true)
    const data = ref({})
    const success = ref(false)
    const running = ref(false)
    return {
      opened,
      closeDialog,
      data,
      success,
      running,
    }
  },
  methods: {
    run (options) {
      this.running = true
      this.axios.post("/_exceptionite/actions/", {"action_id": this.action.id, "options": options}).then(response => {
        this.data = response.data
        this.success = true
      }).catch(error => {
        console.error(error)
        try {
          this.data = error.data
        } catch {

        }
        this.success = false
      }).finally(()=>{
        this.running = false
      })
    }
  }
}
</script>
