<template>
  <div class="flex items-center">
    <button
      class="stack-button mr-2"
      v-for="action in actions" :key="action.id"
      @click="run(action)"
    >
      {{ action.name }}
    </button>
    <p v-if="running">Running ...</p>
    <p v-else-if="message">{{ message }}</p>
    <!-- <button class="stack-button mr-2" @click="selectSupport">Open an issue</button>
    <button class="stack-button mr-2" @click="selectSupport('MasoniteSupport')">Get Masonite support</button>
    <button class="stack-button mr-2" @click="selectSupport">Post on StackOverflow</button> -->
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>