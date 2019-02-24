<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-checkbox
        label="Selected All"
        v-model="selectAll"
        @change="doSelectAll"
      ></v-checkbox>
    </v-flex>
    <v-flex xs4 md3 lg2 v-for="user in group.users" :key="user.id">
      <v-checkbox
        v-model="selected"
        :label="user | username"
        @change="declearChange"
        :value="user.id"
      ></v-checkbox>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: ["value", "group"],
  data() {
    return {
      // select all feture
      selected: value,
      selectAll: false,
      isIndeterminate: true
    };
  },
  methods: {
    // handleCheckAllChange(val) {
    //   // this.value = val ? this.group.users.map(el => el.id) : [];
    //   this.isIndeterminate = false;
    //   this.declearChange();
    // },
    // handleCheckedMemberChange(value) {
    //   console.log(value);
    //   this.declearChange();
    // },
    doSelectAll(val) {
      if (val) {
        this.selected = this.group.users.map(el => el.id);
      } else {
        this.selected = [];
      }
      console.log(this.selected);
      this.declearChange();
    },
    declearChange() {
      this.$emit("input", this.selected);
    }
  },
  computed: {},
  mounted() {}
};
</script>
