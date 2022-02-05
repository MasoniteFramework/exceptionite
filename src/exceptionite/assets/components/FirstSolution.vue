<template>
  <div class="rounded-md bg-green-100 dark:bg-teal-400 p-4">
    <div class="flex items-center mb-4">
      <SolidCheckCircleIcon class="h-5 w-5 dark:text-teal-300 text-green-800 flex-shrink-0" />
      <span class="text-md font-medium dark:text-teal-700 text-green-800 ml-4">{{ solution.title }}</span>
    </div>
    <div class="ml-3">
      <p class="text-sm font-medium text-green-800 dark:text-teal-700">
        {{ solution.description }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "FirstSolution",
  props: {
    solution: {
      type: Object,
      required: true
    }
  }
}
</script>