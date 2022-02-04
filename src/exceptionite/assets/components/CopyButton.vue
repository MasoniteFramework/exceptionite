<template>
    <button title="Copy to clipboard" @click="copy(text)">
        <div v-if="copied" class="bg-indigo-500 dark:bg-gray-900 text-white text-xs px-2 py-1 rounded-md">
          Copied!
        </div>
        <DuplicateIcon
          v-else
          class="h-5 w-5 cursor-pointer text-gray-600 dark:text-gray-400 hover:text-gray-700"
        />
    </button>
</template>

<script>
export default {
  name: "CopyButton",
  props: {
    text: { required: true },
  },
  data: () => ({
    copied: false,
    timeout: false,
  }),
  methods: {
    copy(text) {
      if (this.timeout) {
        window.clearTimeout(this.timeout);
      }
      navigator.clipboard.writeText(text)
      this.copied = true;
      this.timeout = window.setTimeout(() => (this.copied = false), 2000);
    },
  },
};
</script>
