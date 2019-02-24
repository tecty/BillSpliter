<template>
  <v-flex xs12 sm6 md4 lg3 d-flex>
    <v-select
      v-model="value"
      :items="groupList"
      item-value="id"
      item-text="name"
      label="Group"
      @change="declearChange"
    />
  </v-flex>
</template>

<script>
import { mapState } from "vuex";
export default {
  props: ["value"],
  data() {
    return {};
  },
  methods: {
    declearChange() {
      this.$emit("input", this.value);
    }
  },
  computed: {
    ...mapState("group", ["groupList"])
  },
  mounted() {
    this.$store.dispatch("group/require_grouplist");
  }
};
</script>
