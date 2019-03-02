<template>
  <v-data-table :headers="headers" :items="bill" item-key="name">
    <template slot="items" slot-scope="props">
      <td>{{ props.item.title }}</td>
      <td class="text-xs-left">{{ props.item.description }}</td>
      <td class="text-xs-left">{{ props.item.owner.username }}</td>
      <td class="text-xs-center">{{ props.item.state | showState }}</td>
      <td class="text-xs-right">
        <v-btn
          color="success"
          flat
          icon
          :to="{ name: 'billDetail', params: { id: props.item.id } }"
        >
          <v-icon>send</v-icon>
        </v-btn>
      </td>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: {
    bill: Array
  },
  data() {
    return {
      headers: [
        {
          text: "Title",
          align: "left",
          sortable: false,
          value: "name"
        },

        {
          text: "Description",
          align: "left",
          sortable: false
        },
        {
          text: "Owner",
          align: "left",
          sortable: false
        },
        {
          text: "State",
          align: "center",
          sortable: true,
          value: "state"
        },
        {
          text: "Action",
          align: "right",
          sortable: false,
          value: "state"
        }
      ]
    };
  }
};
</script>
