<template>
  <Disclosure :default-open="!!block.has_content" v-slot:default="{ open }">
    <DisclosureButton class="w-full">
      <div class="text-gray-600 dark:text-gray-400 font-medium text-xs uppercase tracking-wide flex items-center justify-between cursor-pointer">
        <div class="flex items-center">
          <component :is="block.icon" class="mr-2 h-4 w-4 text-gray-600" />
          <span>{{ block.name }}</span>
        </div>
        <ChevronUpIcon v-if="open" class="h-5 w-5 text-gray-400" />
        <ChevronDownIcon v-else class="h-5 w-5 text-gray-400" />
      </div>
    </DisclosureButton>
    <DisclosurePanel class="mt-3">
      <alert
        v-for="solution in block.data.solutions" class="mb-2"
        :key="solution.title"
      >
        <template #title>{{ solution.title }}</template>
        <div>{{ solution.description }}</div>
        <a
          v-if="solution.doc_link"
          target="_blank"
          :href="solution.doc_link"
          class="btn btn-solution mt-2"
          v-tooltip="`Open Masonite documentation related to this issue`"
        >
          <SolidInformationCircleIcon class="-ml-0.5 mr-2 h-4 w-4" />
          Open Related Documentation
        </a>
      </alert>
      <p v-if="!block.has_content" class="text-black dark:text-gray-400">{{ block.empty_msg || "No content." }}</p>
    </DisclosurePanel>
  </Disclosure>
</template>

<script>
import Alert from "../Alert.vue"
import {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
  } from '@headlessui/vue'
export default {
  props: {
    block: {
      type: Object,
      required: true
    }
  },
  components: {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    Alert,
  }
}
</script>

<style>

</style>