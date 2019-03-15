<template>
  <v-data-table
    :headers="headers"
    :items="bill"
    item-key="name"
    :loading="loading"
  >
    <template slot="items" slot-scope="props">
      <router-link
        tag="tr"
        :to="{ name: 'billDetail', params: { id: props.item.id } }"
      >
        <td>{{ props.item.title }}</td>
        <td class="text-xs-left">{{ props.item.description }}</td>
        <td class="text-xs-right">{{ props.item.owner | username }}</td>
        <td class="text-xs-right">{{ props.item.state | showState }}</td>
      </router-link>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: {
    bill: Array,
    loading: Boolean
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
  }
};
</script>
