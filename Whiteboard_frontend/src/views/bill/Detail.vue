<template>
  <v-container>
    <v-progress-circular indeterminate v-if="waiting" color="primary" />
    <div v-else>
      <h1>{{ title }}</h1>
      <h5>
        <span class="info--text">{{ bill.state | showState }}</span>
        | {{ bill.created | showDateTime }}
      </h5>
      <h3 class="secondary--text">{{ description }}</h3>
      <v-layout row wrap>
        <v-flex xs12 md10 lg8 mt-2>
          <v-data-table
            :headers="headers"
            :items="transactions"
            hide-actions
            item-key="id"
          >
            <template slot="items" slot-scope="props">
              <td>{{ props.item.from_u | fullnameById(group) }}</td>
              <td>{{ props.item.to_u | fullnameById(group) }}</td>
              <td class="text-xs-right">$ {{ props.item.amount }}</td>
              <td class="text-xs-right">{{ props.item.state | showState }}</td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
      <v-layout row wrap v-if="bill.owner.id == uid">
        <v-btn color="success" v-if="bill.state == 'SP'" @click="resume"
          >resume</v-btn
        >
        <v-btn color="success" v-else @click="suspend">suspend</v-btn>
        <v-btn color="info" disabled>Modify</v-btn>
        <v-btn color="error" @click="remove">Delete</v-btn>
      </v-layout>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
export default {
  data() {
    return {
      waiting: true,
      // the whole entity of this bill
      bill: undefined,
      id: 2,
      title: "hello",
      description: "helloworld",
      transactions: [],
      // group entity bind to this bill
      group: {},
      headers: [
        {
          text: "From User",
          align: "left",
          sortable: false,
          value: "name"
        },

        {
          text: "To User",
          align: "left",
          sortable: false
        },
        {
          text: "Amount",
          align: "right",
          sortable: false
        },
        {
          text: "State",
          align: "right",
          sortable: true,
          value: "state"
        }
      ]
    };
  },
  computed: { ...mapState({ uid: state => state.auth.id }) },
  methods: {
    getBaseUrl(action = "") {
      return `bills/${this.id}/` + action;
    },
    setData(ret) {
      this.waiting = false;

      this.id = ret.data.id;
      this.title = ret.data.title;
      this.description = ret.data.description;
      this.transactions = ret.data.transactions;

      this.bill = ret.data;
      // find the group information
      this.group = this.$store.state.group.groupList.find(
        el => el.id == ret.data.group
      );
    },
    async resume() {
      this.waiting = true;
      let ret = await axios.get(this.getBaseUrl("resume"));
      this.setData(ret);
    },
    async suspend() {
      this.waiting = true;
      let ret = await axios.get(this.getBaseUrl("reject"));
      this.setData(ret);
    },
    async modify() {
      // not implement yet
      return false;
    },
    async remove() {
      // delete this bill
      this.waiting = true;
      await axios.delete(this.getBaseUrl());
      this.$router.push("/bills");
    }
  },
  async mounted() {
    this.$store.dispatch("group/require_grouplist");
    this.id = this.$route.params.id;
    let ret = await axios.get(this.getBaseUrl());
    this.setData(ret);
  }
};
</script>
