<template>
  <!-- state -->
  <template v-if="submitted">
    <alert v-if="success">{{ success }}</alert>
    <alert v-else-if="error">{{ error }}</alert>
  </template>
  <template v-else>
    <!-- description -->
    <p class="text-sm">You can easily share your error page on Masonite debug support. You will then be able
      to provide the link of your page in Masonite Discord community.
    </p>
    <!-- select what data to share -->
    <share-selector v-model="shareOptions" class="my-4"/>
    <button class="stack-button text-right" @click="$emit('run', {options:shareOptions})" v-if="!success && !error" :disabled="running">
      {{ running ? "Sharing..." : "Share" }}
    </button>
  </template>
</template>

<script>
import ShareSelector from "../ShareSelector.vue"
import Alert from "../Alert.vue"

export default {
  name: "MasoniteSupport",
  components: {
    ShareSelector,
    Alert,
  },
  props: {
    success: {
      type: String,
      required: true
    },
    error: {
      type: String,
      required: true
    },
    running: {
      type: Boolean,
      required: true
    }
  },
  emits: ["run", "close"],
  inject: ["shareOptions"],
  computed: {
    submitted () {
      return (!!this.success || !!this.error) && !this.running
    }
  }
}
</script>
