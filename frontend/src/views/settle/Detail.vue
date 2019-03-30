<template>
  <v-container grid-list-xs>
    <div class="text-xs-center" v-if="waiting">
      <v-progress-circular class="center" indeterminate color="primary" />
    </div>
    <div v-else>
      <h1>
        <span class="grey--text darken-1--text font-weight-regular"
          >{{ group.name }} Settlement</span
        >
        {{ settle.title }}
      </h1>
      <h4>
        {{ settle.state | showState }} | {{ settle.created | showDateTime }}
      </h4>
      <h1 v-if="myTr && myTr.state == 'PR'">
        {{ myTr | trToAmount(uid) }}
        <v-btn color="success" @click="approve(myTr.id)">I've Paid</v-btn>
      </h1>
      <h2>{{ settle.description }}</h2>

      <div v-if="settle.state == 'SP'">
        <h2>Waitign Bills</h2>
        <v-flex mt-2 mb-2>
          <BillList :bill="bills" :loading="waitBill" />
        </v-flex>
        <v-layout row wrap v-if="settle.owner.id == uid">
          <v-btn color="info" disabled>Modify</v-btn>
          <v-btn color="error" @click="remove">Delete</v-btn>
        </v-layout>
      </div>
      <div v-else>
        <div v-if="isOwner">
          <h2>Settle Transations</h2>
          <v-flex mt-2 mb-2 xs12 md10 lg8>
            <v-data-table
              :headers="headers"
              :items="settle_tr"
              hide-actions
              item-key="id"
            >
              <template slot="items" slot-scope="props">
                <td>{{ props.item.from_u | fullnameById(group) }}</td>
                <td class="text-xs-center">${{ props.item.amount }}</td>
                <td class="text-xs-right">{{ props.item.state | strState }}</td>
                <td class="text-xs-right">
                  <v-btn
                    color="success"
                    small
                    icon
                    flat
                    @click="approve(props.item.id)"
                    v-if="props.item.state == 'AP'"
                  >
                    <v-icon>done</v-icon>
                  </v-btn>
                  <v-btn
                    color="error"
                    small
                    icon
                    flat
                    @click="reject(props.item.id)"
                    v-if="props.item.state == 'AP'"
                  >
                    <v-icon>not_interested</v-icon>
                  </v-btn>
                </td>
              </template>
            </v-data-table>
          </v-flex>
        </div>
        <h2>Bills</h2>
        <v-flex mt-2 mb-2 xs12 md10 lg8>
          <BillBrief
            :bill="bills"
            :loading="waitBill"
            :settleId="parseInt(this.$route.params.id)"
          />
        </v-flex>
      </div>
    </div>
  </v-container>
</template>

<script>
import BillList from "@/components/bill/List.vue";
import BillBrief from "@/components/bill/BriefList.vue";
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      settle: undefined,
      waiting: true,
      waitBill: true,
      groupId: undefined,
      bills: [],
      title: "",
      settle_tr: [],
      headers: [
        {
          text: "From",
          align: "left",
          sortable: false,
          value: "name"
        },
        {
          text: "Amount",
          align: "center",
          sortable: true,
          value: "amount"
        },
        {
          text: "State",
          align: "right",
          sortable: true,
          value: "state"
        },
        {
          text: "Actions",
          align: "right",
          sortable: false
        }
      ]
    };
  },
  computed: {
    ...mapState("group", ["groupList"]),
    ...mapState("auth", { uid: state => state.id }),
    group: function() {
      let ret = this.groupList.find(el => el.id == this.groupId);
      if (ret) return ret;
      return { name: "" };
    },
    isOwner() {
      return this.uid == this.settle.owner.id;
    },
    myTr: function() {
      if (this.isOwner) {
        return undefined;
      }
      // else
      return this.settle_tr.find(
        el => el.from_u == this.uid || el.to_u == this.uid
      );
    }
  },
  methods: {
    ...mapActions("settle", [
      "s_get",
      "s_get_wait_bill",
      "s_get_incl_bill",
      "s_delete",
      "s_get_stat",
      "str_approve",
      "str_reject"
    ]),
    ...mapActions("group", ["require_grouplist"]),
    async approve(str_id) {
      let ret = await this.str_approve(str_id);
      this.refresh();
      return ret;
    },
    async reject(str_id) {
      let ret = await this.str_reject(str_id);
      this.refresh();
      return ret;
    },
    async refresh() {
      this.require_grouplist();
      let ret = await this.s_get(this.$route.params.id);
      this.settle = ret.data;
      this.groupId = this.settle.group;
      this.settle_tr = this.settle.settle_tr;
      this.waiting = false;
      if (this.settle.state == "SP") {
        // try to fetch the waiting bill
        ret = await this.s_get_wait_bill(this.settle.id);
        this.bills = ret.data;
        this.waitBill = false;
      } else {
        // fetch the included bill
        ret = await this.s_get_incl_bill(this.settle.id);
        this.bills = ret.data;
        this.waitBill = false;
      }
    },
    async remove() {
      await this.s_delete(this.settle.id);
      this.$router.push("/");
    }
  },
  components: {
    BillList,
    BillBrief
  },
  mounted() {
    this.refresh();
  }
};
</script>
