<template>
  <v-container>
    <h1>Create Bill</h1>
    <form @submit.prevent>
      <v-layout row wrap>
        <v-flex xs12 md6 pa-1>
          <v-text-field label="Title" v-model="title"></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 pa-1>
          <v-select
            v-model="group"
            :items="groupList"
            item-value="id"
            item-text="name"
            label="Group"
            return-object
          />
        </v-flex>
      </v-layout>
      <v-layout row wrap>
        <v-flex grow xs12 pa-1>
          <v-text-field
            label="Description"
            v-model="description"
          ></v-text-field>
        </v-flex>
      </v-layout>
      <!-- select phople in the group -->
      <MemberSelector v-if="group" :group="group" v-model="userSelected" />
      {{ userSelected }}
    </form>
  </v-container>
</template>
<script>
// import GroupSelector from "@/components/group/Selector.vue";
import MemberSelector from "@/components/group/MemberSelector.vue";
import { mapState } from "vuex";

export default {
  data() {
    return {
      title: "",
      description: "",
      group: undefined,
      // get uid as the first el
      userSelected: []
    };
  },
  computed: {
    ...mapState("group", ["groupList"])
  },
  components: {
    // GroupSelector,
    MemberSelector
  },
  mounted() {
    this.$store.dispatch("group/require_grouplist");
  }
};
</script>
