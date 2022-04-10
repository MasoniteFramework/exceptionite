<template>
  <div class="grid gap-y-2 gap-x-1 grid-cols-12 p-4 border-t border-gray-300 dark:border-gray-700">
    <template v-for="(value, key) in variables" :label="key" :key="key">
        <span class="text-black dark:text-gray-400 self-center text-sm col-span-2 truncate">{{ key }}</span>
        <pre class="bg-gray-200 col-span-10 dark:bg-gray-900 dark:text-gray-300 break-all rounded-sm p-2 grow group relative" style="white-space: unset;">
          <p
            class="leading-tight text-xs pr-3"
            v-html="highlightCode(value)"
          />
          <CopyButton :text="value" class="absolute right-2 top-1 group-hover:block hidden" />
        </pre>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    variables: {
      type: Object,
      required: true,
    }
  },
  methods: {
    highlightCode (code) {
      return this.$root.highlightCode("python", code)
    }
  },
}
</script>
