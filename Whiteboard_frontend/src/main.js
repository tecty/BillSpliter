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

Vue.filter("fullnameById", (id, group) => {
  // find the user
  let user = group.users.find(el => el.id == id);
  // parse it to have it's full name
  if (user.first_name) return `${user.first_name} ${user.last_name}`;
  else return user.username;
});
Vue.use(Vuetify);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
