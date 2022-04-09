<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-md p-6 w-full text-black mb-4 shadow-md"
    v-for="block in data.blocks"
    :key="block.name"
    :id="block.name"
  >
    <component
      :is="block.component"
      :block="block"
    />
  </div>
</template>

<script>
export default {
  name: "Basic",
  props:{
    data: {
      type: Object,
      required: true
    }
  },
}
</script>
