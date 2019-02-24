<template>
  <v-select
    v-model="value"
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
