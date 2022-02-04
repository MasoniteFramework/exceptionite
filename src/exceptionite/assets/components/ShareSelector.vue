<template>
  <div class="space-y-4">
    <Switch
      v-model="shareOptions.exception.show"
      label="Exception"
    />
    <div class="space-y-2">
      <Switch
        v-model="shareOptions.stacktrace.show"
        label="Stack trace"
        @update:modelValue="updateStackOptions"
      />
      <Switch
        v-if="shareOptions.stacktrace.show"
        v-model="shareOptions.stacktrace.first_frame"
        label="Only first frame"
        class="ml-4"
      />
    </div>
    <Switch
      v-model="shareOptions.context.show"
      @update:modelValue="updateContextOptions"
      label="Context"
    />
    <div class="ml-4 space-y-2" v-if="shareOptions.context.show">
      <div class="relative flex items-start" v-for="section in contextSections" :key="section">
        <div class="flex items-center h-5">
          <input
            v-model="shareOptions.context[section]"
            :id="section"
            :name="section"
            type="checkbox"
            class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
          >
        </div>
        <div class="ml-3 text-sm">
          <label for="comments" class="font-medium ">{{ section }}</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, inject } from "vue"
import Switch from "./Switch.vue"

export default {
  name: "ShareSelector",
  props: {
    modelValue:{
      type: Object,
      required: true
    }
  },
  components: {
    Switch,
  },
  emits: ["update:modelValue"],
  setup (props, ctx) {
    const context = inject("context")
    const contextSections =  context.map(item => item.name)
    const defaultShareOptions = inject("shareOptions")
    const shareOptions = computed({
      get () {
        return props.modelValue
      },
      set (value) {
        ctx.emit("update:modelValue", value)
      },
    })
    shareOptions.value = defaultShareOptions
    return {
      shareOptions,
      contextSections
    }
  },
  methods: {
    updateStackOptions (show) {
      if (!show) {
        this.shareOptions.stacktrace.first_frame = false
      }
    },
    updateContextOptions (show) {
      if (!show) {
        Object.keys(this.contextSections).forEach(section => {
          this.shareOptions.context[section] = false
        })
      }
    }
  }
}
</script>
