<template>
  <v-container>
    <h1>{{ name }}'s Profile</h1>
    <h2>User ID: {{ id }}</h2>
    <h2>User Name: {{ username }}</h2>
  </v-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";
export default {
  computed: {
    ...mapGetters("auth", ["name"]),
    ...mapState("auth", ["id", "username"])
  }
};
</script>
