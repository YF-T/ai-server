<template>
  <pre :class="[languageClass]" class="codeviewer" :key="code">
    <code v-html="highlighted"></code>
  </pre>
</template>
<script setup lang="ts">
import { highlight, languages } from 'prismjs'
import { computed } from 'vue'
const { code, language } = defineProps<{
    code: string, 
    language: string,
}>()
const prismLanguage = languages[language]
const languageClass =`language-${language}`
const highlighted = computed(() => highlight(code, prismLanguage, language))
</script>
<style>
.token.operator {
    background: none !important;
}

.codeviewer {
  width: auto;
  overflow-x: scroll;
}

pre[class*="language-"]:before {
  box-shadow: none !important;
}

pre[class*="language-"]:after {
  box-shadow: none !important;
}
</style>
