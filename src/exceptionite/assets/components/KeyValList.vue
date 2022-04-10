<template>
  <div :class="className">
    <h3 v-if="title" class="text-left text-blue-600 font-medium mb-2">{{ title }}</h3>
    <dl v-if="$slots.default" class="definition-list items-baseline">
      <slot></slot>
    </dl>
    <div v-if="!$slots.default" class="definition-list">
      <div class="definition-list-empty">—</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: { default: '' },
    className: { default: '' },
  },
}
</script>

<style>

</style>