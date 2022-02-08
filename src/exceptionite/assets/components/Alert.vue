<template>
  <div class="rounded-md bg-green-200 dark:ring-1 dark:ring-inset dark:ring-white/10 p-4 dark:bg-blue-800">
    <div class="flex items-center mb-2">
      <div class="flex-shrink-0">
        <SolidCheckCircleIcon class="h-5 w-5 text-green-400 dark:text-gray-300" />
      </div>
      <div class="ml-2">
        <p class="text-sm font-medium text-green-800 dark:text-gray-300">
          <slot name="title"/>
        </p>
      </div>
    </div>
    <div>
      <p class="text-sm text-green-700 dark:text-gray-300">
        <slot />
      </p>
    </div>
  </div>
</template>

