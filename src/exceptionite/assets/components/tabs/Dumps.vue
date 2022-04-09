<template>
  <div class="bg-white dark:bg-gray-800 rounded-md p-6 w-full text-black dark:text-gray-400 shadow-md mb-4">
    <div v-for="dump in dumps" :key="dump">
      <div class="flex items-center mb-2">
        <span class="badge badge-indigo mr-2">{{ dump.locale_time }}</span>
        <span class="badge badge-gray">{{ dump.relative_file }} : {{ dump.line }}</span>
        <span class="text-xs font-medium ml-4">{{ dump.method }}()</span>
      </div>
      <div class="grid gap-y-2 gap-x-1 grid-cols-12 p-4 pr-0 border-t border-gray-300 dark:border-gray-700">
        <template v-for="(obj, obj_name) in dump.objects" :label="obj_name" :key="obj_name">
            <span class="text-black dark:text-gray-400 self-baseline text-sm col-span-2 truncate font-medium">{{ obj_name }}</span>
            <div class="col-span-10">
              <pre class="bg-gray-200 col-span-10 dark:bg-gray-900 break-all rounded-sm p-2 grow group relative" style="white-space: unset;">
                <p
                  class="leading-tight text-xs pr-3"
                  v-html="highlightCode(obj.value)"
                />
                <CopyButton :text="obj.value" class="absolute right-2 top-1 group-hover:block hidden" />
              </pre>
              <Disclosure as="template" v-slot="{ open }" v-if="Object.keys(obj.properties.public).length > 0">
                <DisclosureButton as="div" class="text-indigo-500 text-xs font-medium my-2 cursor-pointer flex items-center">
                  <SolidMinusSmIcon class="h-4 w-4" v-if="open" />
                  <SolidPlusSmIcon class="h-4 w-4" v-else />
                  <span class="ml-1">Public Properties</span>
                </DisclosureButton>
                <DisclosurePanel as="div" class="grid gap-y-2 gap-x-1 grid-cols-12">
                  <template v-for="(prop, prop_name) in obj.properties.public" :label="prop_name" :key="prop_name">
                      <span class="text-black dark:text-gray-400 self-center text-sm col-span-2 truncate">{{ prop_name }}</span>
                      <pre class="bg-gray-200 col-span-10 dark:bg-gray-900 break-all rounded-sm p-2 grow group relative" style="white-space: unset;">
                        <p
                          class="leading-tight text-xs pr-3"
                          v-html="highlightCode(prop)"
                        />
                        <CopyButton :text="getCodeAsString(prop)" class="absolute right-2 top-1 group-hover:block hidden" />
                      </pre>
                  </template>
                </DisclosurePanel>
              </Disclosure>
              <Disclosure as="template" v-slot="{ open }" v-if="Object.keys(obj.properties.private).length > 0">
                <DisclosureButton as="div" class="text-indigo-500 text-xs font-medium my-2 cursor-pointer flex items-center">
                  <SolidMinusSmIcon class="h-4 w-4" v-if="open" />
                  <SolidPlusSmIcon class="h-4 w-4" v-else />
                  <span class="ml-1">Private Properties</span>
                </DisclosureButton>
                <DisclosurePanel as="div" class="grid gap-y-2 gap-x-1 grid-cols-12">
                  <template v-for="(prop, prop_name) in obj.properties.private" :label="prop_name" :key="prop_name">
                      <span class="text-black dark:text-gray-400 self-center text-sm col-span-2 truncate">{{ prop_name }}</span>
                      <pre class="bg-gray-200 col-span-10 dark:bg-gray-900 break-all rounded-sm p-2 grow group relative" style="white-space: unset;">
                        <p
                          class="leading-tight text-xs pr-3"
                          v-html="highlightCode(prop)"
                        />
                        <CopyButton :text="getCodeAsString(prop)" class="absolute right-2 top-1 group-hover:block hidden" />
                      </pre>
                  </template>
                </DisclosurePanel>
              </Disclosure>
            </div>
        </template>
      </div>
    </div>
    <p v-if="!data.has_content">Nothing dumped !</p>
  </div>
</template>

<script>
import { ref } from "vue"
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from '@headlessui/vue'

export default {
  name: "DumpsTab",
  components: {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
  },
  props:{
    data: {
      type: Object,
      required: true
    }
  },
  setup () {
    const getCodeAsString = (code) => {
      let codeString = code.toString()
      if (typeof code === "object") {
        codeString = JSON.stringify(code)
      }
      return codeString
    }
    const dumps = ref([])
    return {
      getCodeAsString,
      dumps
    }
  },
  inject: ["config"],
  created () {
    //transform stack trace
    this.dumps = this.data.data.dumps.map(dump => {
      let relativePath = dump.filename.replace(`${this.config.options.absolute_path}/`, '')
      return {
        ...dump,
        locale_time: new Date(dump.timestamp * 1000).toLocaleTimeString(),
        relative_file: relativePath,
      }
    })
  },
  methods: {
    highlightCode (code) {
      return this.$root.highlightCode("python", this.getCodeAsString(code))
    }
  }
}
</script>
