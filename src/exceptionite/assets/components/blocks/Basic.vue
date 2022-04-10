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
      <key-val-list
        v-if="!block.has_sections"
        class-name="tab-content-section"
      >
        <key-val-item v-for="(value, key) in block.data" :label="key" :key="key" :value="value" />
      </key-val-list>
      <key-val-list
        v-else
        v-for="(subblock, title) in block.data"
        :key="title"
        :title="title"
        :id="title"
        class-name="tab-content-section mb-6"
      >
        <key-val-item v-for="(value, key) in subblock" :label="key" :key="key" :value="value" />
      </key-val-list>
      <p v-if="!block.has_content" class="text-black dark:text-gray-400">{{ block.empty_msg || "No content." }}</p>
    </DisclosurePanel>
  </Disclosure>
</template>

<script>
import KeyValList from "@/components/KeyValList.vue"
import KeyValItem from "@/components/KeyValItem.vue"

import {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
  } from '@headlessui/vue'
export default {
  components: {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    KeyValList,
    KeyValItem,
  },
  props: {
    block: {
      type: Object,
      required: true
    }
  },
}
</script>
