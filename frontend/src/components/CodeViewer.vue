<template>
  <pre :class="[languageClass, 'line-numbers']">
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
const languageClass =`language-${language}`
const highlighted = highlight(code, prismLanguage, language)
</script>
<style>
.token.operator {
    background: none !important;
}
</style>
