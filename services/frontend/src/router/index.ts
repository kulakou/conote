// @ts-ignore
import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
    { path: "/", name: "Home", component: Home },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        // Always scroll to top
        return { top: 0 };
    },
});

export default router;
