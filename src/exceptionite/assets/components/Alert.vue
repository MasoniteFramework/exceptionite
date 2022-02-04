<template>
  <div class="rounded-md bg-green-50 p-4">
    <div class="flex">
      <div class="flex-shrink-0">
        <SolidCheckCircleIcon class="h-5 w-5 text-green-400" />
      </div>
      <div class="ml-3">
        <p class="text-sm font-medium text-green-800">
          <slot />
        </p>
      </div>
    </div>
  </div>
</template>