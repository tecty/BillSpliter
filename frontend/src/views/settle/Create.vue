<template>
  <v-container>
    <h1>Create Bill</h1>
    <form @submit.prevent="submit">
      <v-layout row wrap>
        <v-flex xs12 md7 lg7 pa-1>
          <v-text-field label="Title" v-model="title"></v-text-field>
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex grow xs12 pa-1>
          <v-text-field label="Description" v-model="description" />
        </v-flex>
      </v-layout>
      <!-- select phople in the group -->
      <v-layout row wrap>
        <v-flex xs12 md6 lg3 pa-1>
          <GroupSelector v-model="group" />
        </v-flex>
      </v-layout>

      <v-layout row wrap>
        <v-btn color="success" type="submit">Settle It!</v-btn>
      </v-layout>
    </form>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
import GroupSelector from "@/components/group/Selector.vue";

export default {
  data() {
    return {
      title: "",
      description: "",
      group: undefined
    };
  },
  methods: {
    ...mapActions("settle", ["s_create"]),
    async submit() {
      await this.s_create({
        title: this.title,
        description: this.description,
        group: this.group.id
      });
      this.$router.push({
        name: "settle"
      });
    }
  },
  mounted() {},
  components: {
    GroupSelector
  }
};
</script>
