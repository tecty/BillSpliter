<template>
  <v-container grid-list-xs12>
    <h1>
      Settlement
      <v-btn color="success" flat icon :to="{ name: 'settleCreate' }">
        <v-icon>add</v-icon>
      </v-btn>
    </h1>
    <v-layout row wrap>
      <v-flex xs12 md10 lg8 mt-2>
        <v-data-table
          :headers="headers"
          :items="settle"
          item-key="name"
          hide-actions
        >
          <template slot="items" slot-scope="props">
            <router-link
              tag="tr"
              :to="{ name: 'settleDetail', params: { id: props.item.id } }"
            >
              <td>
                {{ props.item.title }}
                <br />
                <span class="secondary--text">{{
                  props.item.description
                }}</span>
              </td>
              <td>{{ props.item.group | idToGroupName(groupList) }}</td>
              <td>{{ props.item.created | showDateTime }}</td>
            </router-link>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import { mapActions, mapState } from "vuex";
export default {
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
          text: "Group",
          align: "right",
          sortable: false
        },
        {
          text: "Time",
          align: "right",
          sortable: true,
          value: "created"
        }
      ],
      settle: []
    };
  },
  computed: {
    ...mapState("group", ["groupList"])
  },
  methods: {
    ...mapActions("settle", ["s_get"]),
    ...mapActions("group", ["require_grouplist"])
  },
  async mounted() {
    this.require_grouplist();
    let ret = await this.s_get();
    this.settle = ret.data;
  }
};
</script>
