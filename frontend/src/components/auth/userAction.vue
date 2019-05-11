<template>
  <v-menu offset-y v-model="menu">
    <v-btn flat v-if="username" slot="activator">{{ username }}</v-btn>
    <iterList :items="items" v-model="menu" />
  </v-menu>
</template>

<script>
import { mapState } from "vuex";
import iterList from "@/components/helper/IterList";

export default {
  data: () => ({
    actions: [],
    menu: false
  }),
  computed: {
    ...mapState({
      fullname: state => `${state.auth.first_name}  ${state.auth.last_name}`,
      username: state => state.auth.username
    }),
    get_language_item() {
      return { icon: "", title: "English" };
      // return { icon: "", title: "Chinese" };
    },
    items() {
      return [
        { icon: "group", title: "Group", href: "group" },
        { icon: "person", title: "Profile", href: "profile" },
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
