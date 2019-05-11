<template>
  <v-app id="inspire">
    <v-navigation-drawer
      fixed
      abolute
      clipped
      class="grey lighten-4"
      app
      v-model="drawer"
    >
      <iterList :items="items" />
    </v-navigation-drawer>
    <v-toolbar dark color="light-blue darken-2" app clipped-left tabs>
      <v-toolbar-side-icon
        @click.native="drawer = !drawer"
      ></v-toolbar-side-icon>
      <router-link
        :to="{ name: 'home' }"
        style="text-decoration: none; color:#FFF"
      >
        <v-toolbar-title>Whiteboard</v-toolbar-title>
      </router-link>
      <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-btn v-if="!username" flat :to="{ name: 'login' }">Login</v-btn>
        <userAction v-else />
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import userAction from "@/components/auth/userAction";
import iterList from "@/components/helper/IterList";
export default {
  name: "App",
  components: {
    userAction,
    iterList
  },
  data() {
    return {
      drawer: false,
      items: [
        // { icon: "touch_app", text: "Reminders", href: "about" },
        { heading: "Billing System", text: "create", href: "billCreate" },
        { icon: "call_made", text: "Transactions", href: "transaction" },
        { icon: "merge_type", text: "Bills", href: "bill" },
        { icon: "shuffle", text: "Settlement", href: "settle" },
        { divider: true },
        { icon: "settings", text: "Settings", href: "about" },
        { icon: "person", text: "User", href: "profile" },
        { icon: "group", text: "Group", href: "group" },
        { icon: "help", text: "Help" },
        { icon: "phonelink", text: "App downloads" },
        { icon: "keyboard", text: "Keyboard shortcuts" }
      ]
    };
  },
  computed: {
    ...mapState({
      username: state => state.auth.username
    })
  },
  methods: {
    ...mapActions({
      logoutInVuex: "clear_all"
    }),
    logout() {
      this.logoutInVuex();
      this.$router.push("/");
    }
  }
};
</script>

<style>
h1,
h2,
h3,
h4,
h5 {
  font-weight: 300 !important;
}
.v-btn {
  margin: 0;
}
</style>
