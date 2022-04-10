<template>
  <div class="stack-main-content relative rounded-r-md">
    <span class="badge absolute top-2 right-2 badge-gray">{{ frame.relative_file }} ({{ frame.method }}) : {{ frame.no }}</span>
    <div class="stack-viewer scrollbar">
        <div class="stack-ruler">
            <div class="stack-lines">
                <p
                    v-for="(code, line_number) in frame.content"
                    :key="line_number"
                    class="stack-line cursor-pointer"
                    :class="{
                        'stack-line-highlight':
                            parseInt(line_number) === frame.no,
                    }"
                >
                    {{ line_number }}
                </p>
            </div>
        </div>
        <pre
          :class="$root.theme"
          class="hljs stack-code overflow-y-auto dark:bg-gray-800" ref="codeContainer">
          <div
            v-for="(code, line_number) in frame.content"
            :key="line_number"
            :class="{
                'stack-code-line-highlight': parseInt(line_number) === frame.no,
            }"
            class="stack-code-line cursor-pointer"
            @click="openEditor(line_number)"
            v-html="highlightCode(code)"
          />
        </pre>
    </div>
  </div>
</template>

<script>
import url from "../editorUrl"
export default {
  name: "Frame",
  props: {
    frame: {
      type: Object,
      required: true
    }
  },
  inject: ["config"],
  methods: {
    highlightCode(code) {
      return this.$root.highlightCode(this.frame.language, code);
    },
    openEditor (line_number) {
      window.open(url(this.config.options.editor, this.frame.file, line_number))
    }
  }
}
</script>
