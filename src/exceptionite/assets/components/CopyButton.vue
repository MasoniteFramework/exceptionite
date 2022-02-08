<template>
  <button title="Copy to clipboard" @click="copy(text)">
    <CheckIcon v-if="copied" class="h-4 w-4 text-green-600" />
    <DuplicateIcon
      v-else
      class="h-4 w-4 cursor-pointer text-gray-500 dark:text-gray-400 hover:text-gray-700"
    />
  </button>
</template>

<script>
import { useClipboard } from "@vueuse/core"

export default {
  name: "CopyButton",
  props: {
    text: { required: true },
  },
  setup () {
    const { copy, copied } = useClipboard({ copiedDuring: 2000})
    return {
      copy,
      copied
    }
  }
}
</script>
