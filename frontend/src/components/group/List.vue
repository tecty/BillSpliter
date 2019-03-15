<template>
  <v-data-table :headers="headers" :items="groupList" item-key="name">
    <template slot="items" slot-scope="props">
      <router-link
        tag="tr"
        :to="{ name: 'groupDetail', params: { id: props.item.id } }"
      >
        <td>{{ props.item.name }}</td>
        <td class="text-xs-right">{{ props.item.owner.username }}</td>
        <td class="text-xs-right">{{ props.item.name_list }}</td>
      </router-link>
    </template>
  </v-data-table>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
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
  computed: {
    ...mapState({ groupList: state => state.group.groupList })
  },
  methods: {},
  mounted() {
    this.$store.dispatch("group/require_grouplist");
  }
};
</script>
