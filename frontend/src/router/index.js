import Vue from "vue";
import Router from "vue-router";
import AppHome from "@/views/Home.vue";
import { isLogin } from "@/utils/auth";
import group from "./group.js";
import bill from "./bill.js";
import settle from "./settle.js";
Vue.use(Router);

// main route list
var routeLists = [
  {
    path: "/",
    name: "home",
    component: AppHome,
    meta: {
      // key to let the view can be view from guest
      guest: true
    }
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/About.vue"),
    meta: {
      // key to let the view can be view from guest
      guest: true
    }
  },
  {
    path: "/login",
    name: "login",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */
      "@/views/auth/Login.vue"),
    meta: {
      // key to let the view can be view from guest
      guest: true
    },
    beforeEnter: (to, from, next) => {
      // if user is currently logged in, prevent him from hitting this page.
      if (isLogin()) {
        next("/");
      } else {
        // go to next
        next();
      }
    }
  },
  {
    path: "/register",
    name: "register",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */
      "@/views/auth/Register.vue"),
    meta: {
      // key to let the view can be view from guest
      guest: true
    },
    beforeEnter: (to, from, next) => {
      // if user is currently logged in, prevent him from hitting this page.
      if (isLogin()) {
        next("/");
      } else {
        // go to next
        next();
      }
    }
  }
];

// acquire the routes sotre in seperate files
routeLists.push(...group);
routeLists.push(...bill);
routeLists.push(...settle);
// routeLists.push(...post);
// routeLists.push(...profile);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: routeLists
});