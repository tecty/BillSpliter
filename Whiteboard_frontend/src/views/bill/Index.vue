<template>
  <v-container>
    <h1>Bills<v-btn color="success">Cretae</v-btn></h1>
    <h2>Processing Bills</h2>
    <BillList type="processing" />
    <h2 class="mt-3">Related Bills</h2>
    <BillList type="related" />
  </v-container>
</template>
<script>
import BillList from "@/components/bill/List.vue";
export default {
  data() {
    return {};
  },
  components: {
    BillList
  }
};
</script>
