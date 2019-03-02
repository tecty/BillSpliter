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
      <v-list dense class="grey lighten-4">
        <template v-for="(item, i) in items">
          <v-layout row v-if="item.heading" align-center :key="i">
            <v-flex xs6>
              <v-subheader v-if="item.heading">{{ item.heading }}</v-subheader>
            </v-flex>
            <v-flex xs6 class="text-xs-right" v-if="item.text">
              <v-btn
                small
                flat
                :to="item.href ? { name: item.href } : null"
                class="grey--text"
                >{{ item.text }}</v-btn
              >
            </v-flex>
          </v-layout>
          <v-divider
            dark
            v-else-if="item.divider"
            class="my-3"
            :key="i"
          ></v-divider>
          <v-list-tile
            :key="i"
            v-else
            :to="item.href ? { name: item.href } : null"
          >
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title class="grey--text">
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar color="light-blue darken-2" app clipped-left tabs>
      <v-toolbar-side-icon
        @click.native="drawer = !drawer"
      ></v-toolbar-side-icon>
      <v-toolbar-title to="{name:'home'}">Whiteboard</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn v-if="!username" to="login" flat>Login</v-btn>
        <userAction v-else />
        <v-btn v-if="username" @click="logout" flat>Logout</v-btn>
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
export default {
  name: "App",
  components: {
    userAction
  },
  data() {
    return {
      drawer: false,
      items: [
        // { icon: "touch_app", text: "Reminders", href: "about" },
        { heading: "Billing System", text: "create", href: "billCreate" },
        { icon: "call_made", text: "Transactions", href: "transaction" },
        { icon: "merge_type", text: "Bills", href: "bill" },
        { icon: "shuffle", text: "Settlement" },
        { divider: true },
        { icon: "settings", text: "Settings", href: "about" },
        { icon: "person", text: "User" },
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
</style>
