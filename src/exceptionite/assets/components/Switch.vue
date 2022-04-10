<template>
<SwitchGroup>
  <div class="flex items-center">
    <ExtSwitch
      v-model="value"
      :class='value ? "bg-blue-600" : "bg-gray-200 dark:bg-gray-900"'
      class="relative inline-flex items-center h-6 transition-colors rounded-full w-11 focus:outline-none"
    >
      <span
        :class='value ? "translate-x-6" : "translate-x-1"'
        class="inline-block w-4 h-4 transition-transform transform bg-white dark:bg-gray-300 rounded-full"
      />
    </ExtSwitch>
    <SwitchLabel class="ml-2 text-sm">{{ label }}</SwitchLabel>
  </div>
</SwitchGroup>
</template>

<script>
import { computed } from "vue"
import { Switch as ExtSwitch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
export default {
  name: "Switch",
  components: {
    ExtSwitch, SwitchGroup, SwitchLabel,
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      required: true
    }
  },
  emits: ["update:modelValue"],
  setup (props, context) {
    const value = computed({
      get () {
        return props.modelValue
      },
      set (value) {
        context.emit("update:modelValue", value)
      },
    })
    return {
      value
    }
  }
}
</script>
