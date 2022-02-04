<template>
  <div class="sticky top-28 rounded-md p-2">
    <div v-for="block in menu" :key="block.name" class="mb-8">
      <a
        :href="`#${block.name}`"
        class="text-gray-600 dark:text-gray-400 font-medium text-xs uppercase tracking-wide mb-3 flex items-center cursor-pointer"
      >
        <component :is="block.icon" class="mr-2 h-4 w-4 text-gray-600" />
        <span>{{ block.name }}</span>
      </a>
      <div v-if="block.component=='KeyValBlockWithSections'">
        <a
          v-for="(data, subblock) in block.data"
          :key="subblock"
          class="block text-gray-500 dark:text-gray-400 text-sm mb-2 hover:text-indigo-500"
          :href="`#${subblock}`"
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
  }
}
</script>
