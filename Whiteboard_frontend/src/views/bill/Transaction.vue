<template>
  <v-container>
    <v-progress-circular indeterminate v-if="waiting" color="primary" />
    <div v-else>
      <h1>
        Transactions
        <v-btn color="success" flat>
          <v-icon>done_all</v-icon>Approve All
        </v-btn>
      </h1>
      <h2>Ongoing Transactions</h2>
      <v-data-table
        :headers="headers"
        :items="ongoing"
        item-key="name"
        hide-actions
      >
        <template slot="items" slot-scope="props">
          <router-link
            tag="td"
            :to="{ name: 'billDetail', params: { id: props.item.bill } }"
          >
            {{ props.item.title }}
            <span class="text--secondary">{{ props.item.description }}</span>
          </router-link>
          <td class="text-xs-right">
            {{ props.item.to_u | fullnameById(group) }}
          </td>
          <td class="text-xs-right">$ {{ props.item.amount }}</td>
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

      <v-btn color="success" flat> <v-icon>done</v-icon>Approve </v-btn>
      <v-btn color="error" flat> <v-icon>not_interested</v-icon>Reject </v-btn>
      <h2>Concencused Transactions</h2>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import { mapState, mapActions } from "vuex";

export default {
  data() {
    return {
      ongoing: [],
      concencus: [],
      waiting: true,
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
      ]
    };
  },
  computed: {
    ...mapState({
      group: state => {
        let ret = state.group.groupList.reduce(function(acc, curr) {
          return [...acc, ...curr.users];
        }, []);
        return { users: ret };
      }
    })
  },
  methods: {
    ...mapActions("bill", ["b_approve", "b_reject"]),
    removeOngoingById(id) {
      let index = this.ongoing.findIndex(el => el.id == id);
      this.ongoing.splice(index, 1);
    },
    async approve(id) {
      await this.b_approve(id);
      this.removeOngoingById(id);
    },
    async reject(id) {
      await this.b_reject(id);
      this.removeOngoingById(id);
    }
  },
  async mounted() {
    this.$store.dispatch("group/require_grouplist");

    let ret = await axios.get("brief_tr");
    this.waiting = false;
    this.ongoing = ret.data.filter(el => el.state == "PR");
    this.concencus = ret.data.filter(el => el.state == "CS");
  }
};
</script>
