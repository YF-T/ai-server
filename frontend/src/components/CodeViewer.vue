<template>
  <pre :class="[languageClass]" class="codeviewer" >
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

.codeviewer {
  width: 100%;
}

pre[class*="language-"]:before {
  box-shadow: none !important;
}

pre[class*="language-"]:after {
  box-shadow: none !important;
}
</style>
