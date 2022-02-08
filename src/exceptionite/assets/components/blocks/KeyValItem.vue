<template>
  <dd class="text-black dark:text-gray-400 text-sm truncate">
    {{ label }}
  </dd>
  <dt class="group">
    <slot>
      <div class="relative bg-gray-200 dark:bg-gray-900 dark:text-gray-300 p-2 rounded-sm text-xs break-all leading-tight pr-8">
        <span v-if="value">{{ value }}</span>
        <span v-else class="text-gray-400 dark:text-gray-600">-</span>
        <CopyButton v-if="value" :text="'default' in $slots && $slots.default()[0].children" class="absolute right-2 origin-center top-0 translate-y-1/2 group-hover:block hidden" />
      </div>
    </slot>
  </dt>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      required: true
    },
    value: {
      type: [String, null, Object, Array, Boolean],
      required: true
    }
  }
}
</script>
