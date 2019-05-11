<template>
  <v-menu offset-y>
    <v-btn flat v-if="username" slot="activator">{{ username }}</v-btn>
    <iterList :items="items" />
  </v-menu>
</template>

<script>
import { mapState } from "vuex";
import iterList from "@/components/helper/IterList";

export default {
  data: () => ({
    actions: [],
    items: [
      { icon: "group", text: "Group", href: "group" },
      { icon: "person", text: "Profile", href: "profile" },
      { icon: "shuffle", text: "Language" },
      { icon: "shuffle", text: "Logout", href: "logout" }
    ]
  }),
  computed: {
    ...mapState({
      fullname: state => `${state.auth.first_name}  ${state.auth.last_name}`,
      username: state => state.auth.username
    })
  },
  components: {
    iterList
  }
};
</script>
