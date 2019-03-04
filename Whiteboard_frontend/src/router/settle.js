export default [
  {
    path: "/settles",
    name: "settle",
    component: () => import("@/views/settle/Index.vue")
  },
  {
    path: "/settles/create",
    name: "settleCreate",
    component: () => import("@/views/settle/Create.vue")
  },
  {
    path: "/settles/:id",
    name: "settleDetail",
    component: () => import("@/views/settle/Detail.vue")
  }
];
