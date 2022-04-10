<template>
  <div class="bg-white dark:bg-gray-800 p-8 rounded-md relative">
    <div class="text-red-600 font-bold">{{ exception.type }}</div>
    <div class="text-black dark:text-gray-300 text-2xl">{{ exception.message }}</div>
    <span class="badge absolute top-2 right-2 badge-gray">{{ exception.namespace }}</span>
    <CopyButton :text="`${exception.type}: ${exception.message}`" class="absolute right-2 bottom-2" />
  </div>
</template>

<script>
export default {
  name: "Exception",
  props: {
    exception: {
      type: Object,
      required: true
    }
  }
}
</script>
