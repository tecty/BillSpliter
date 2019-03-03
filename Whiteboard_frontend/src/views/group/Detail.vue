<template>
  <v-container grid-list-xs>
    <v-progress-circular indeterminate v-if="waiting" color="primary"/>
    <div v-else>
      <h1>{{ name }}</h1>
      <h3>
        <strong>Owner:</strong>
        {{ owner | username }}
      </h3>
      <h2>Users</h2>
      <ul>
        <li v-for="u in users" :key="u.id">{{ u | username }}</li>
      </ul>
      <v-form v-if="isOwner" @submit.prevent="addUser">
        <v-text-field label="User ID" v-model="newUid" required/>
        <v-btn color="success" type="submit">Add User</v-btn>
      </v-form>
    </div>
  </v-container>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  data() {
    return {
      waiting: true,
      id: undefined,
      name: "",
      owner: undefined,
      users: [],
      newUid: undefined
    };
  },
  computed: {
    ...mapState("auth", { uid: state => state.id }),
    isOwner() {
      return this.uid == this.owner.id;
    }
  },
  methods: {
    ...mapActions("group", ["g_get_group", "g_add_user"]),
    addUser() {
      this.g_add_user({
        uid: this.newUid,
        gid: this.id
      });
      this.refreshData();
    },
    async refreshData() {
      let res = await this.$store.dispatch(
        "group/g_get_group",
        this.$route.params.id
      );
      this.waiting = false;
      this.name = res.data.name;
      this.owner = res.data.owner;
      this.users = res.data.users;
      this.id = res.data.id;
    }
  },
  async mounted() {
    this.refreshData();
  }
};
</script>
