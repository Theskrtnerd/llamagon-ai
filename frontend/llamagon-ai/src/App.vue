<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <ul>
    <li><RouterLink to="/">HelloWorld</RouterLink></li>
    <li><RouterLink to="/pdfjs">PDFjs</RouterLink></li>
  </ul>
  <RouterView />
</template>
