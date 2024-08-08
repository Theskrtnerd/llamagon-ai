import { createWebHistory, createRouter } from "vue-router";

import Pdfjs from "./components/PDFjs.vue";
import HelloWorld from "./components/HelloWorld.vue";

const routes = [
    { path: "/", component: HelloWorld },
  { path: "/pdfjs", component: Pdfjs },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
