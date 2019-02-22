import index from "@/views/group/Index.vue";
export default {
  path: "/group",
  name: "group",
  component: index,
  children: [
    {
      path: "create",
      name: "create",
      component: () => import("@/views/group/Create.vue")
    }
  ]
};
