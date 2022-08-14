<template>
  <pre :class="className">
    <code v-html="highlighted" ></code>
  </pre>
</template>
<script setup lang="ts">
import { highlight, languages } from 'prismjs'

const { code, language } = defineProps<{
    code: string, 
    language: string,
}>()
const prismLanguage = languages[language]
const className =`language-${language}`
const highlighted = highlight(code, prismLanguage, language)
</script>
<style scoped>
</style>
