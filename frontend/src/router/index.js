import Vue from "vue";
import Router from "vue-router";
import auth from "./auth";
import group from "./group.js";
import bill from "./bill.js";
import settle from "./settle.js";
import profile from "./profile.js";
Vue.use(Router);

// main route list
var routeLists = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/Home.vue"),
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
  }
];

// acquire the routes sotre in seperate files
routeLists.push(...group);
routeLists.push(...bill);
routeLists.push(...settle);
routeLists.push(...auth);
routeLists.push(...profile);

// vue route instance
let _router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: routeLists
});

// router guard for login
_router.beforeEach((to, from, next) => {
  if (to.matched.some(record => !record.meta.guest)) {
    // this route is required auth
    if (localStorage.getItem("token")) {
      next();
    } else {
      next({
        name: "login",
        query: {
          redirect: to.fullPath
        }
      });
    }
  } else {
    // this page is not login required
    next();
  }
});

export default _router;
