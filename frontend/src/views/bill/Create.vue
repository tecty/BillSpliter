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
        <v-flex grow xs12 md6 lg4 pa-1>
          <v-text-field
            type="number"
            label="Total"
            v-model="total"
            prefix="$"
            placeholder="xx.xx"
          />
        </v-flex>
        <v-flex xs12 md6 lg3 pa-1>
          <GroupSelector v-model="group" />
        </v-flex>
      </v-layout>

      <MemberSelector v-if="group" :group="group" v-model="userSelected" />
      <v-layout row wrap>
        <v-btn color="success" type="submit">Split it!</v-btn>
      </v-layout>
    </form>
  </v-container>
</template>
<script>
import GroupSelector from "@/components/group/Selector.vue";
import MemberSelector from "@/components/group/MemberSelector.vue";

export default {
  data() {
    return {
      title: "",
      description: "",
      group: undefined,
      // get uid as the first el
      userSelected: [parseInt(localStorage.getItem("uid"))],
      total: undefined
    };
  },
  methods: {
    async submit() {
      let portion = this.total / this.userSelected.length;
      // to elimiate the bug of creating two decimal place
      portion = portion.toFixed(2);

      let ret = await window.axios.post("bills/", {
        title: this.title,
        description: this.description,
        group: this.group.id,
        transactions: this.userSelected.map(el => ({
          from_u: el,
          amount: portion
        }))
      });
      // success return
      this.$router.push({ name: "billDetail", params: { id: ret.data.id } });
    }
  },
  components: {
    GroupSelector,
    MemberSelector
  }
};
</script>
