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
    <v-toolbar color="blue" dark fixed app clipped-left :flat="is_flat">
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
    <ButtonGroupChoice />
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";
import userAction from "@/components/auth/userAction";
import iterList from "@/components/helper/IterList";
import ButtonGroupChoice from "@/components/helper/ButtonGroupChoice";
export default {
  name: "App",
  components: {
    userAction,
    iterList,
    ButtonGroupChoice
  },
  data() {
    return {
      drawer: false,
      items: [
        {
          icon: "library_books",
          title: "Billing",
          href: "billCreate",
          items: [
            { icon: "call_made", title: "Transactions", href: "transaction" },
            { icon: "merge_type", title: "Bills", href: "bill" },
            { icon: "shuffle", title: "Settlement", href: "settle" }
          ]
        },
        {
          icon: "domain",
          title: "Users",
          items: [
            { icon: "person", title: "User Profile", href: "profile" },
            { icon: "group", title: "Group", href: "group" }
          ]
        },
        { icon: "settings", title: "Settings", href: "about" },
        { icon: "help", title: "Help" },
        { icon: "phonelink", title: "App downloads" },
        { icon: "keyboard", title: "Keyboard shortcuts" }
      ]
    };
  },
  computed: {
    ...mapState({
      username: state => state.auth.username
    }),
    is_flat() {
      return this.$route.name == "home";
    }
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
