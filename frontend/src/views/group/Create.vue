<template>
  <v-container>
    <h1>Create Group</h1>
    <form @submit.prevent="submit">
      <v-layout row wrap>
        <v-flex xs6>
          <v-text-field label="Group Name" v-model="group" required autofocus />
        </v-flex>
      </v-layout>
      <v-btn color="success" type="submit">Create</v-btn>
    </form>
  </v-container>
</template>
<script>
export default {
  data() {
    return {
      group: undefined
    };
  },
  methods: {
    async submit() {
      let ret = await window.axios.post("groups/", {
        name: this.group
      });
      // success return
      this.$router.push({ name: "groupDetail", params: { id: ret.data.id } });
    }
  }
};
</script>
