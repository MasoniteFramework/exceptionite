<template>
<!-- bg-green-100 text-green-800 -->
  <span
    class="inline-flex items-center px-2 py-1.5 rounded text-xs font-medium"
    :class="`bg-${color}-100 text-${color}-800 dark:bg-${darkColor}-100 dark:text-${darkColor}-800`"
  >
    <slot />
  </span>
</template>

<script>
export default {
  name: "Badge",
  props: {
    color: {
      type: String,
      default: "gray"
    },
    darkColor: {
      type: String,
      default: "green"
    }
  }
}
</script>

<style>

</style>