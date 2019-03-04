<template>
  <v-container grid-list-xs>
    <div class="text-xs-center" v-if="waiting">
      <v-progress-circular class="center" indeterminate color="primary" />
    </div>
    <div v-else>
      <h1>
        <span class="grey--text darken-1--text font-weight-regular"
          >{{ settle.group | idToGroupName(groupList) }} Settlement</span
        >
        {{ settle.title }}
      </h1>
      <h3>
        {{ settle.state | showState }} | {{ settle.created | showDateTime }}
      </h3>
      {{ settle }}
      <div>
        <h2>Transations</h2>
      </div>

      <div v-if="settle.state == 'SP'">
        <h2>Waitign Bills</h2>
        <BillList :bill="bills" :loading="waitBill" />
      </div>
      <div v-else>
        <h2>Bills</h2>
      </div>
    </div>
  </v-container>
</template>

<script>
import BillList from "@/components/bill/List.vue";
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      settle: undefined,
      waiting: true,
      waitBill: true,
      bills: [],
      title: ""
    };
  },
  computed: {
    ...mapState("group", ["groupList"]),
    ...mapState("auth", { uid: state => state.id })
  },
  methods: {
    ...mapActions("settle", ["s_get", "s_get_wait_bill"]),
    ...mapActions("group", ["require_grouplist"])
  },
  components: {
    BillList
  },
  async mounted() {
    this.require_grouplist();
    let ret = await this.s_get(this.$route.params.id);
    this.settle = ret.data;
    this.waiting = false;
    if (this.settle.state == "SP") {
      // try to fetch the waiting bill
      ret = await this.s_get_wait_bill(this.settle.id);
      this.bills = ret.data;
      this.waitBill = false;
    } else {
      // fetch the included bill
      ret = await this.s_get_wait_bill(this.settle.id);
      this.bills = ret.data;
      this.waitBill = false;
    }
  }
};
</script>
