import {createRouter, createWebHistory} from "vue-router";


const routes = [
    {
        meta: {
            title: "lfcity-站点首页",
            keepalive: true
        },
        path: "/",
        name: "Home",
        component: () => import("../views/Home.vue")
    },
    {
        meta: {
            title: "lfcity-登录页面",
            keepalive: true
        },
        path: "/login",
        name: "Login",
        component: () => import("../views/Login.vue")
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

export default router;