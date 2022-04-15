<template>
  <div class="rounded-md bg-yellow-50 dark:ring-1 dark:ring-inset dark:ring-white/10 p-4 dark:bg-yellow-600">
    <div class="flex items-center mb-2">
      <div class="flex-shrink-0">
        <SolidExclamationCircleIcon class="h-5 w-5 text-yellow-400 dark:text-yellow-900" />
      </div>
      <div class="ml-2">
        <p class="text-md font-medium text-yellow-600 dark:text-yellow-900">
          No solution proposed for your error ?
        </p>
      </div>
      <div class="ml-auto pl-3">
        <div class="-mx-1.5 -my-1.5">
          <button type="button" @click="$emit('click')" class="inline-flex bg-transparent rounded-md p-1.5 text-yellow-600 dark:text-yellow-900 hover:bg-yellow-100 focus:outline-none dark:hover:bg-yellow-700">
            <span class="sr-only">Dismiss</span>
            <XIcon class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
    <div>
      <p class="text-sm text-yellow-700 dark:text-yellow-900">
        It looks like we have not found a solution for this error. You can request to display a solution for this
        error if you want by clicking the button below.
      </p>
      <a
        target="_blank"
        :href="link"
        class="btn btn-no-solution mt-2"
        v-tooltip="`Open an issue to add a solution for this exception`"
      >
        <SolidInformationCircleIcon class="-ml-0.5 mr-2 h-4 w-4" />
        Open a Solution Request
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "NoSolution",
  props: {
    link: {
      type: String,
      required: true
    }
  },
  emits: ["click"]
}
</script>