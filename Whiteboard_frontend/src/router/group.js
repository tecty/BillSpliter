export default [
  {
    path: "/group",
    name: "group",
    component: () => import("@/views/group/Index.vue")
  },
  {
    path: "/group/create",
    name: "groupCreate",
    component: () => import("@/views/group/Create.vue")
  },
  {
    path: "/group/:id",
    name: "groupDetail",
    component: () => import("@/views/group/Detail.vue")
  }
];
