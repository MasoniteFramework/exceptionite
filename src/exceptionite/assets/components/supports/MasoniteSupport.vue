<template>
  <!-- state -->
  <template v-if="submitted">
    <alert v-if="success">Your error has been shared on Masonite support website !</alert>
    <p>You can access it here: <a :href="data.data.link" class="underline text-blue-600 text-sm">{{ data.data.link }}</a> with the given ID:</p>
    <div class="bg-gray-200 dark:bg-gray-900 dark:text-gray-300 p-2 rounded-sm text-xs relative break-all leading-tight pr-8">{{ data.id }}</div>
  </template>
  <template v-else>
    <!-- description -->
    <p class="text-sm">You can easily share your error page on Masonite debug support. You will then be able
      to provide the link of your page in Masonite Discord community.
    </p>
    <!-- select what data to share -->
    <share-selector v-model="shareOptions" class="my-4"/>
    <button class="btn text-right" @click="$emit('run', {options:shareOptions})" v-if="!success && !error" :disabled="running">
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
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
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
      return this.success && !this.running
    }
  }
}
</script>
