<template>
  <v-container>
    <v-progress-circular indeterminate v-if="waiting" color="primary" />
    <div v-else>
      <h1>
        Transactions
        <v-btn color="success" flat @click="approve_all">
          <v-icon>done_all</v-icon>Approve All
        </v-btn>
      </h1>
      <div v-if="ongoing.length != 0">
        <h2>Approveable Transactions</h2>
        <v-layout row wrap>
          <v-flex xs12 md10 lg8 mt-2 mb-2>
            <v-data-table
              :headers="headers"
              :items="ongoing"
              item-key="name"
              hide-actions
            >
              <template slot="items" slot-scope="props">
                <router-link
                  tag="tr"
                  :to="{ name: 'billDetail', params: { id: props.item.bill } }"
                >
                  {{ props.item.title }}
                  <span class="text--secondary">
                    {{ props.item.description }}
                  </span>
                </router-link>
                <td class="text-xs-right">
                  {{ props.item.to_u | fullnameById(group) }}
                </td>
                <td class="text-xs-right">${{ props.item.amount }}</td>
                <td class="text-xs-left">
                  <v-btn
                    color="success"
                    small
                    icon
                    flat
                    @click="approve(props.item.bill)"
                  >
                    <v-icon>done</v-icon>
                  </v-btn>
                  <v-btn
                    color="error"
                    small
                    icon
                    flat
                    @click="reject(props.item.bill)"
                  >
                    <v-icon>not_interested</v-icon>
                  </v-btn>
                </td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>
      </div>

      <h2>Well Accepted Transactions</h2>
      <v-layout row wrap>
        <v-flex xs12 md10 lg8 mt-2 mb-2>
          <v-data-table
            :headers="concencusHeader"
            :items="concencus"
            item-key="name"
            hide-actions
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">
                {{ props.item.from_u | fullnameById(group) }}
              </td>
              <td class="text-xs-left">
                {{ props.item.to_u | fullnameById(group) }}
              </td>
              <td class="text-xs-right">{{ props.item | trAmount }}</td>
              <router-link
                tag="td"
                class="text-xs-right"
                :to="{ name: 'billDetail', params: { id: props.item.bill } }"
              >
                {{ props.item.title }}
                <br />
                <span class="text--secondary">
                  {{ props.item.description }}
                </span>
              </router-link>
            </template>
            <template v-slot:footer>
              <td></td>
              <td class="text-xs-left">Balance</td>
              <td class="text-xs-right">${{ balance }}</td>
              <td></td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      transactions: [],
      waiting: true,
      balance: 0,
      headers: [
        {
          text: "Bill",
          align: "left",
          sortable: false,
          value: "name"
        },

        {
          text: "To User",
          align: "right",
          sortable: false
        },
        {
          text: "Amount",
          align: "right",
          sortable: true,
          value: "amount"
        },
        {
          text: "Actions",
          align: "right",
          sortable: false
          // value: "state"
        }
      ],
      concencusHeader: [
        {
          text: "From",
          align: "left",
          sortable: false
        },
        {
          text: "To",
          align: "left",
          sortable: false
        },
        {
          text: "Amount",
          align: "right",
          sortable: true,
          value: "amount"
        },
        {
          text: "Bill",
          align: "right",
          sortable: false,
          value: "name"
        }
      ]
    };
  },
  computed: {
    ...mapState("auth", { uid: state => state.id }),
    ...mapState({
      group: state => {
        let ret = state.group.groupList.reduce(function(acc, curr) {
          return [...acc, ...curr.users];
        }, []);
        return { users: ret };
      }
    }),
    ongoing() {
      return this.transactions.filter(
        el => el.from_u == this.uid && el.state == "PR"
      );
    },
    concencus() {
      if (this.waiting) {
        return [];
      }

      return this.transactions.filter(
        el => el.state == "CS" || el.state == "CD"
      );
    }
  },
  methods: {
    ...mapActions("bill", ["b_approve", "b_reject", "b_approve_all"]),
    removeOngoingById(id) {
      let index = this.ongoing.findIndex(el => el.id == id);
      this.ongoing.splice(index, 1);
    },
    async approve(id) {
      await this.b_approve(id);
      this.refreshData();
    },
    async reject(id) {
      await this.b_reject(id);
      this.refreshData();
    },
    async approve_all() {
      await this.b_approve_all();

      this.refreshData();
    },
    async refreshData() {
      let ret = await Promise.all([
        axios.get("brief_tr/"),
        axios.get("bills/balance/")
      ]);
      // assign the balances
      this.balance = ret[1].data.balance;
      // update the tr list
      this.transactions = ret[0].data;
      this.waiting = false;
      return ret;
    }
  },
  mounted() {
    Promise.all([
      this.$store.dispatch("group/require_grouplist"),
      this.refreshData()
    ]);
  }
};
</script>
