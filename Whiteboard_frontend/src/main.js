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

Vue.use(Vuetify);
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
