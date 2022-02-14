<template>
  <div class="sticky top-28 rounded-md p-2">
    <div v-for="block in menu" :key="block.name" class="mb-8">
      <a
        @click="$emit('browse', block.name)"
        class="text-gray-600 dark:text-gray-400 font-medium text-xs uppercase tracking-wide mb-3 flex items-center cursor-pointer"
      >
        <component :is="block.icon" class="mr-2 h-5 w-5 text-gray-600 dark:text-blue-500" />
        <span class="text-gray-500 dark:text-gray-400 hover:text-blue-500 dark:hover:text-gray-300">{{ block.name }}</span>
      </a>
      <div v-if="block.component=='KeyValBlockWithSections'" class="ml-6">
        <a
          v-for="(data, subblock) in block.data"
          :key="subblock"
          class="block text-gray-500 dark:text-gray-400 text-sm mb-2 hover:text-blue-500 dark:hover:text-gray-300 hover:cursor-pointer"
          @click="$emit('browse', subblock)"
        >
          {{ subblock }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ContextMenu",
  props: {
    menu: {
      type: Array,
      required: true
    }
  },
  emits: ["browse"],
}
</script>
