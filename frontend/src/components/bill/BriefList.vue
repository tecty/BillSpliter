<template>
  <v-data-table
    :headers="headers"
    :items="bill"
    item-key="name"
    :loading="loading"
    hide-actions
  >
    <template slot="items" slot-scope="props">
      <router-link
        tag="tr"
        :to="{ name: 'billDetail', params: { id: props.item.id } }"
      >
        <td>{{ props.item.title }}</td>
        <td class="text-xs-right">{{ props.item.owner | username }}</td>
        <td class="text-xs-right">{{ props.item | billToAmount(uid) }}</td>
      </router-link>
    </template>
    <template slot="footer" v-if="settleId">
      <tr>
        <td>Balance</td>
        <td></td>
        <td class="text-xs-right">{{ balance | showAmount }}</td>
      </tr>
      <tr>
        <td>Actual Spent</td>
        <td></td>
        <td class="text-xs-right">{{ actual_pay | showAmount }}</td>
      </tr>
      <tr>
        <td>Transaction Count</td>
        <td></td>
        <td class="text-xs-right">{{ tr_count }}</td>
      </tr>
      <tr>
        <td>GDP</td>
        <td></td>
        <td class="text-xs-right">{{ gdp | showAmount }}</td>
      </tr>
    </template>
  </v-data-table>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  props: {
    bill: Array,
    loading: Boolean,
    settleId: Number
  },
  data() {
    return {
      gdp: undefined,
      tr_count: undefined,
      balance: undefined,
      actual_pay: undefined,
      headers: [
        {
          text: "Title",
          align: "left",
          sortable: false,
          value: "name"
        },

        {
          text: "Owner",
          align: "right",
          sortable: false
        },

        {
          text: "amount",
          align: "right",
          sortable: false
        }
      ]
    };
  },
  methods: {
    ...mapActions("settle", ["s_get_stat"])
  },

  computed: {
    ...mapState("auth", { uid: state => state.id })
  },
  async mounted() {
    if (this.settleId) {
      let ret = await this.s_get_stat(this.settleId);
      ret = ret.data;
      this.gdp = ret.gdp;
      this.tr_count = ret.tr_count;
      this.balance = ret.balance;
      this.actual_pay = ret.actual_pay;
    }
  }
};
</script>
