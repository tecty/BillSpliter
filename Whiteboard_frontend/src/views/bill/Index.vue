<template>
  <v-container>
    <h1>
      Bills
      <v-btn color="success" flat icon :to="{ name: 'billCreate' }">
        <v-icon>add</v-icon>
      </v-btn>
    </h1>
    <BillList :bill="curr_bill" loading />
  </v-container>
</template>
<script>
import BillList from "@/components/bill/List.vue";
export default {
  data() {
    return {
      curr_bill: [],
      curr_bill_loading: true
    };
  },
  components: {
    BillList
  },
  mounted() {
    this.$store.dispatch("bill/get_curr_bill").then(res => {
      this.curr_bill = res.data;
      this.curr_bill_loading = false;
    });
  }
};
</script>
