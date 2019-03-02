<template>
  <v-container>
    <h1>
      <span class="info--text">#{{ id }}</span>
      {{ title }}
    </h1>
    <h3 class="secondary--text">{{ description }}</h3>
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
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
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
  async mounted() {
    this.$store.dispatch("group/require_grouplist");

    let ret = await axios.get(`bills/${this.$route.params.id}`);

    this.id = ret.data.id;
    this.title = ret.data.title;
    this.description = ret.data.description;
    this.transactions = ret.data.transactions;

    this.bill = ret.data;
    // find the group information
    this.group = this.$store.state.group.groupList.find(
      el => el.id == ret.data.group
    );
  }
};
</script>
