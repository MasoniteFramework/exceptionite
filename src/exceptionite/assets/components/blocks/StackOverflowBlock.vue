<template>
  <div>
    <a :href="item.link" class="block mb-2 underline text-blue-600 text-sm" target="_blank" :key="item.question_id" v-for="item in block.data.questions">{{ item.title }}</a>
  </div>
</template>

<script>
export default {
  props: {
    block: {
      type: Object,
      required: true
    }
  }
}
</script>
