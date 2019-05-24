<template>
  <v-menu offset-y>
    <v-btn flat v-if="name" slot="activator">{{ name }}</v-btn>
    <iterList :items="items" />
  </v-menu>
</template>

<script>
import { mapGetters } from "vuex";
import iterList from "@/components/helper/IterList";

export default {
  data: () => ({
    actions: []
  }),
  computed: {
    ...mapGetters("auth", ["name"]),
    get_language_item() {
      // return { icon: "translate", title: "English" };
      return { icon: "translate", title: "中文" };
    },
    items() {
      return [
        { group_choice: true },
        { icon: "person", title: "User Profile", href: "profile" },
        this.get_language_item,
        { icon: "shuffle", title: "Logout", href: "logout" }
      ];
    }
  },
  components: {
    iterList
  }
};
</script>
