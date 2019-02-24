export default [
  {
    path: "/bills",
    name: "bill",
    component: () => import("@/views/bill/Index.vue")
  },
  // {
  //   path: "/bills/:id",
  //   name: "billDetail",
  //   component: () => import("@/views/bill/Detail.vue")
  // },
  {
    path: "/bills/create",
    name: "billCreate",
    component: () => import("@/views/bill/Create.vue")
  }
];
