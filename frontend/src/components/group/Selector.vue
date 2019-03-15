<template>
  <v-select
    v-model="group"
    :items="groupList"
    item-value="id"
    item-text="name"
    label="Group"
    return-object
    @change="declearChange"
  />
</template>

<script>
import { mapState } from "vuex";
export default {
  props: ["value"],
  data() {
    return {
      group: undefined
    };
  },
  methods: {
    declearChange() {
      this.$emit("input", this.group);
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
