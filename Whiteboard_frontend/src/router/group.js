export default [
  {
    path: "group/",
    name: "group",
    component: () => import("@/views/group/Index.vue"),
    children: [
      {
        path: "create",
        name: "create",
        component: () => import("@/views/group/Create.vue")
      }
    ]
  }
];
