<template>
  <div class="rounded-md bg-green-50 dark:bg-teal-500 p-4">
    <div class="flex">
      <div class="flex-shrink-0">
        <SolidCheckCircleIcon class="h-5 w-5 text-teal-700" />
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium text-green-900 dark:text-teal-800">
          <slot />
        </p>
      </div>
    </div>
  </div>
</template>