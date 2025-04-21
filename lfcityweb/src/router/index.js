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
    {
        meta: {
            title: "lfcity-注册页面",
            keepalive: true
        },
        path: "/register",
        name: "Register",
        component: () => import("../views/Register.vue")
    },
    {
        meta: {
            title: "lfcity-个人中心",
            keepalive: true,
            authorization: true,
        },
        path: "/user",
        name: "User",
        component: () => import("../views/User.vue"),
        children: [
            {
                meta: {
                    title: "lfcity-订单列表",
                    keepalive: true,
                    authorization: true,
                },
                path: "order",
                name: "User-Order",
                component: () => import("../components/user/Order.vue"),
            },
            {
                meta: {
                    title: "lfcity-课程列表",
                    keepalive: true,
                    authorization: true,
                },
                path: "course",
                name: "User-Course",
                component: () => import("../components/user/Course.vue"),
            },
        ]
    },
    {
        meta: {
            title: "lfcity-项目课",
            keepalive: true,
        },
        path: "/project",
        name: "Project",
        component: () => import("../views/Course.vue")
    },
    {
        meta: {
            title: "lfcity-课程详情",
            keepalive: true,
        },
        path: "/detail/:id(\\d+)",
        name: "Detail",
        component: () => import("../views/Detail.vue")
    },
    {
        meta: {
            title: "lfcity-购物车",
            keepalive: true,
            authorization: true,
        },
        path: "/cart",
        name: "Cart",
        component: () => import("../views/Cart.vue")
    },
    {
        meta: {
            title: "lfcity-订单处理",
            keepalive: true,
            authorization: true,
        },
        path: "/order",
        name: "Order",
        component: () => import("../views/Order.vue")
    },
    {
        meta: {
            title: "lfcity-支付成功",
            keepalive: true,
            authorization: true,
        },
        path: "/feedback",
        name: "Feedback",
        component: () => import("../views/Feedback.vue")
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

import store from "../store/index.js";
router.beforeEach((to, from, next)=>{
    // console.log(to.meta.title, to.meta.authorization, store.getters.getUserInfo);
    if(to.meta.authorization && !store.getters.getUserInfo){
        next({"name": "Login"});
    }else{
        next();
    }
})

export default router;