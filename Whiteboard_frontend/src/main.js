import moment from "moment";
import Vue from "vue";
import "./plugins/axios";
import "./plugins/vuetify";
import App from "./App.vue";
import router from "@/router";
import store from "./store";
import "./registerServiceWorker";
import Vuetify from "vuetify";

Vue.config.productionTip = false;

// set up some handy filter
function parseAmount(amount) {
  amount = parseFloat(amount).toFixed(2);
  return `$${amount}`;
}

Vue.filter("username", user => {
  if (user.first_name) return `${user.first_name} ${user.last_name}`;
  else return user.username;
});

Vue.filter("showState", state => {
  let map = {
    PR: "Prepare",
    AP: "Approved",
    RJ: "Rejected",
    CS: "Concencus",
    CD: "Commited",
    FN: "Finish",
    SP: "Suspend"
  };
  return map[state];
});

Vue.filter("strState", state => {
  let map = {
    PR: "Waiting",
    AP: "Paid",
    RJ: "Rejected",
    CS: "Received",
    CD: "Commited",
    FN: "Finish",
    SP: "Suspend"
  };
  return map[state];
});

Vue.filter("fullnameById", (id, group) => {
  // find the user
  let user = group.users.find(el => el.id == id);
  // parse it to have it's full name
  if (user.first_name) return `${user.first_name} ${user.last_name}`;
  else return user.username;
});

Vue.filter("showDateTime", s => {
  return moment(s).format("YYYY MMM DD,h:mm");
});

Vue.filter("trAmount", tr => {
  if (tr.from_u == localStorage.getItem("uid")) return parseAmount(-tr.amount);
  else return parseAmount(tr.amount);
});
Vue.filter("idToGroupName", (id, group) => {
  return group.find(el => el.id == id).name;
});

Vue.filter("billToAmount", (bill, uid) => {
  let amount = 0;
  if (bill.owner.id == uid) {
    amount = bill.transactions
      .filter(el => el.from_u != uid)
      .reduce((sum, el) => sum + parseFloat(el.amount), 0.0);
  } else {
    let tr = bill.transactions.find(el => el.from_u == uid);
    if (tr) {
      amount = -tr.amount;
    }
  }
  return parseAmount(amount);
});

Vue.filter("trToAmount", (tr, uid) => {
  if (tr.from_u == uid) {
    return parseAmount(-tr.amount);
  } else return parseAmount(tr.amount);
});

Vue.filter("showAmount", parseAmount);

Vue.use(Vuetify);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
