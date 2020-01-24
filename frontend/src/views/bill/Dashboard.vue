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

      <v-switch v-model="isSelfSpent">
        <template v-slot:label>
          <h3 v-if="!isSelfSpent" class="black--text">
            Well Accepted Transactions
          </h3>
          <h3 v-else class="black--text">
            Actual Spent Transactions
          </h3>
        </template>
      </v-switch>
      <v-layout row wrap>
        <v-flex xs12 md10 lg8 mt-2 mb-2>
          <v-data-table
            :headers="concencusHeader"
            :items="choosedList"
            item-key="name"
          >
            <template slot="items" slot-scope="props">
              <router-link
                tag="td"
                class="text-xs-left"
                :to="{ name: 'billDetail', params: { id: props.item.bill } }"
              >
                {{ props.item.title }}
                <br />
                <span class="text--secondary">
                  {{ props.item.description }}
                </span>
              </router-link>
              <td class="text-xs-right">
                {{ props.item.by_u | fullnameById(group) }}
              </td>

              <td class="text-xs-right">{{ props.item | trAmount }}</td>
            </template>
            <template v-slot:footer>
              <tr>
                <td></td>
                <td class="text-xs-right">Balance</td>
                <td class="text-xs-right">${{ balance }}</td>
              </tr>
              <tr>
                <td></td>
                <td class="text-xs-right">Actual Spent</td>
                <td class="text-xs-right">${{ spentAmount }}</td>
              </tr>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </div>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      transactions: [],
      isSelfSpent: false,
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
          text: "Bill",
          align: "left",
          sortable: false,
          value: "name"
        },
        {
          text: "By User",
          align: "right",
          sortable: false
        },
        {
          text: "Amount",
          align: "right",
          sortable: true,
          value: "amount"
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
      return this.transactions
        .map(el => {
          if (el.from_u != this.uid) {
            el.by_u = el.from_u;
          } else if (el.to_u != this.uid) {
            el.by_u = el.to_u;
          } else {
            el.by_u = this.uid;
          }
          return el;
        })
        .filter(el => el.state == "CS" || el.state == "CD");
    },
    flowList() {
      return this.concencus.filter(el => el.by_u != this.uid);
    },
    selfSpent() {
      return this.concencus.filter(el => el.from_u == this.uid);
    },
    choosedList() {
      if (this.isSelfSpent) {
        return this.selfSpent;
      } else {
        return this.flowList;
      }
    },
    spentAmount() {
      return -this.selfSpent
        .map(el => parseFloat(el.amount))
        .reduce((acc, a) => acc + a, 0.0)
        .toFixed(2);
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
        window.axios.get("brief_tr/"),
        window.axios.get("bills/balance/")
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
