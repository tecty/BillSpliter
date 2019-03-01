<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-checkbox
        label="Selected All"
        v-model="selectAll"
        @change="doSelectAll"
        :indeterminate="isIndeterminate"
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
      selected: this.value,
      selectAll: false
      // isIndeterminate: true
    };
  },
  methods: {
    doSelectAll(val) {
      if (val) {
        this.selected = this.group.users.map(el => el.id);
      } else {
        this.selected = [];
      }
      // this.isIndeterminate = false;
      // console.log(this.selected);
      this.declearChange();
    },
    declearChange() {
      if (this.group.users.length == this.selected.length) {
        this.selectAll = true;
      } else {
        this.selectAll = false;
      }
      this.$emit("input", this.selected);
      // this.$emit("update:value", this.selected);
    }
  },
  computed: {
    isIndeterminate() {
      // console.log(this.group.users);
      // console.log(this.selected);
      return !(
        this.group.users.length == this.selected.length ||
        this.selected.length == 0
      );
    }
  },
  mounted() {}
};
</script>
