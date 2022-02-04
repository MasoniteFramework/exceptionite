<template>
  <template v-if="submitted">
    <alert v-if="success">{{ success }}</alert>
    <alert v-else-if="error">{{ error }}</alert>
  </template>
  <template v-else>
    <!-- description -->
    <p class="text-sm">You can create an issue on the Masonite GitHub repository.</p>
    <!-- select what data to share -->
    <share-selector v-model="shareOptions" class="my-4"/>

    <div class="space-y-2 my-4">
      <input name="title" v-model="form.title" />
      <textarea name="description" v-model="form.description" />
    </div>

    <button class="stack-button text-right" @click="$emit('run', {options: shareOptions, form})" v-if="!success && !error" :disabled="running">
      {{ running ? "Creating..." : "Create issue" }}
    </button>
  </template>
</template>

<script>
import ShareSelector from "../ShareSelector.vue"
import { ref, inject } from "vue"
import Alert from "../Alert.vue"

export default {
  name: "GitHubSupport",
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
  setup () {
    const exception = inject("exception")
    const form = ref({
      title: `${exception.type} - ${exception.message}`,
      description: ""
    })
    return {
      form,
    }
  },
  computed: {
    submitted () {
      return (!!this.success || !!this.error) && !this.running
    }
  }
}
</script>
