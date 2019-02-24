<template>
  <v-data-table :headers="headers" :items="groupList" item-key="name">
    <template slot="items" slot-scope="props">
      <td>{{ props.item.name }}</td>
      <td class="text-xs-right">{{ props.item.owner.username }}</td>
      <td class="text-xs-right">{{ props.item.name_list }}</td>
    </template>
  </v-data-table>
</template>

<script>
export default {
  data() {
    return {
      props: {
        bill: Array,
        loading: Boolean
      },
      headers: [
        {
          text: "Name",
          align: "left",
          sortable: false,
          value: "name"
        },
        {
          text: "owner",
          align: "right",
          sortable: false,
          value: "name_list"
        },
        {
          text: "Users",
          align: "right",
          sortable: false,
          value: "name_list"
        }
      ]
    };
  },
  methods: {}
};
</script>
