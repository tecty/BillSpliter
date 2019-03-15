import Vue from "vue";
import Vuex from "vuex";
import auth from "./auth.js";
import group from "./group.js";
import bill from "./bill.js";
import settle from "./settle.js";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {
    API_ERROR: (state, error) => {
      state.api_state = "ERROR";
      // claim an error
      state.error = error;
    },
    API_WAITING: state => {
      state.api_state = "WAIT";
    },
    API_FINISHED: state => {
      state.api_state = "";
    },
    API_READY: state => {
      state.api_state = "READY";
    }
  },
  actions: {
    clear_all: ({ commit }) => {
      // console.log(dispatch)
      commit("group/RESET");
      commit("auth/RESET");
    }
  },
  modules: {
    auth,
    group,
    bill,
    settle
  }
});
