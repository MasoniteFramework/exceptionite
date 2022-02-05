<template>
  <Disclosure :default-open="true" v-slot:default="{ open }">
    <DisclosureButton class="w-full">
      <div class="text-gray-600 font-medium text-xs uppercase tracking-wide flex items-center justify-between cursor-pointer">
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
        <span class="font-medium text-md">{{ solution.title }}</span>: {{ solution.description }}
      </alert>
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