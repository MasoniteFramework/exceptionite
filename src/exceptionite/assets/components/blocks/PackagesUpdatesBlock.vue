<template>
  <Disclosure :default-open="true" v-slot:default="{ open }">
    <DisclosureButton class="w-full">
      <div class="text-gray-600 dark:text-gray-400 font-medium text-xs uppercase tracking-wide flex items-center justify-between cursor-pointer">
        <div class="flex items-center">
          <component :is="block.icon" class="mr-2 h-4 w-4 text-gray-600 dark:text-gray-400" />
          <span>{{ block.name }}</span>
        </div>
        <ChevronUpIcon v-if="open" class="h-5 w-5 text-gray-400" />
        <ChevronDownIcon v-else class="h-5 w-5 text-gray-400" />
      </div>
    </DisclosureButton>
    <DisclosurePanel class="mt-3">
      <div
        v-for="(versions, packageName) in block.data"
        :key="packageName"
        class="rounded-md dark:bg-blue-400 bg-blue-100 p-4 mb-2"
      >
        <div class="flex">
          <div class="flex-shrink-0">
            <SolidInformationCircleIcon class="h-5 w-5 text-blue-700" />
          </div>
          <div class="ml-3 flex-1 md:flex md:justify-between">
            <p class="text-sm text-blue-700"><span class="font-medium">{{ packageName }}</span> can be updated from {{ versions.current }} to {{ versions.latest }} !</p>
          </div>
        </div>
      </div>

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