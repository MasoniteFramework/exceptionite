<template>
  <div class="rounded-md bg-green-200 dark:ring-1 dark:ring-inset dark:ring-white/10 p-4 dark:bg-blue-800">
    <div class="flex items-center mb-2">
      <div class="flex-shrink-0">
        <SolidCheckCircleIcon class="h-5 w-5 text-green-400 dark:text-gray-300" />
      </div>
      <div class="ml-2">
        <p class="text-md font-medium text-green-800 dark:text-gray-300">
          {{ solution.title }}
        </p>
      </div>
    </div>
    <div>
      <p class="text-sm text-green-700 dark:text-gray-300">
        {{ solution.description }}
      </p>
      <a
        v-if="solution.doc_link"
        target="_blank"
        :href="solution.doc_link"
        class="btn btn-solution mt-2"
        v-tooltip="`Open Masonite documentation related to this issue`"
      >
        <SolidInformationCircleIcon class="-ml-0.5 mr-2 h-4 w-4" />
        Open Related Documentation
      </a>
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