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
            <v-flex xs6 class="text-xs-right">
              <v-btn small flat>edit</v-btn>
            </v-flex>
          </v-layout>
          <v-divider
            dark
            v-else-if="item.divider"
            class="my-3"
            :key="i"
          ></v-divider>
          <v-list-tile :key="i" v-else :to="item.href">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title class="grey--text">{{
                item.text
              }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar color="light-blue darken-2" app clipped-left>
      <v-toolbar-side-icon
        @click.native="drawer = !drawer"
      ></v-toolbar-side-icon>
      <span class="title ml-3 mr-5">Whiteboard</span>
      <v-spacer></v-spacer>
      <v-btn v-if="!username" to="login" flat>Login</v-btn>
      <v-btn v-else @click="logout" flat>Logout</v-btn>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height class="grey lighten-4">
        <router-view />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "App",
  components: {},
  data() {
    return {
      drawer: false,
      items: [
        { icon: "lightbulb_outline", text: "Notes" },
        { icon: "touch_app", text: "Reminders", href: "about" },
        { divider: true },
        { heading: "Labels" },
        { icon: "add", text: "Create new label" },
        { divider: true },
        { icon: "archive", text: "Archive" },
        { icon: "delete", text: "Trash" },
        { divider: true },
        { icon: "settings", text: "Settings" },
        { icon: "chat_bubble", text: "Trash" },
        { icon: "help", text: "Help" },
        { icon: "phonelink", text: "App downloads" },
        { icon: "keyboard", text: "Keyboard shortcuts" }
      ]
    };
  },
  computed: {
    ...mapState(["username"])
  },
  methods: {
    ...mapActions({
      logoutInVuex: "logout"
    }),
    logout() {
      this.logoutInVuex();
      this.$router.push("/");
    }
  }
};
</script>
