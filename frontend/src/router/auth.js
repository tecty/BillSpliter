export default [
  {
    path: "/auth/login/",
    name: "login",
    meta: {
      guest: true,
      title: "Login"
    },
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/auth/Login.vue")
  },
  {
    path: "/auth/logout/",
    name: "logout",
    meta: {
      guest: true,
      title: "Logout"
    },
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/auth/Logout.vue")
  },
  {
    path: "/auth/register/",
    name: "register",
    meta: {
      guest: true,
      title: "Register"
    },
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/auth/Register.vue")
  }
];
