<template>
  <dd class="text-black dark:text-gray-400 text-sm truncate">
    {{ label }}
  </dd>
  <dt class="group relative">
    <slot>
      <div class="bg-gray-200 dark:bg-gray-900 dark:text-gray-300 p-2 rounded-sm text-xs relative break-all leading-tight pr-8">{{ value }}</div>
    </slot>
    <CopyButton :text="'default' in $slots && $slots.default()[0].children" class="absolute right-2 top-1 group-hover:block hidden" />
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
