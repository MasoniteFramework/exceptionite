<template>
  <button @click="handle">
    <slot />
  </button>
</template>

<script>
export default {
  methods: {
    handle () {
      console.log("clicked !")
    }
  }
}
</script>