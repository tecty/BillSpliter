import Vue from "vue";
import Vuex from "vuex";
import auth from "./auth.js";
import group from "./group.js";
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
    },
    CLEAR_ALL: ({ commit }) => {
      commit("group/RESET");
      commit("auth/RESET");
    }
  },
  actions: {},
  modules: {
    auth,
    group
  }
});
