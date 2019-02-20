import axios from "axios";

export default {
  state: {
    id: "",
    username: "",
    first_name: "",
    last_name: ""
  },
  mutations: {
    ADD_TOKEN: (state, token) => {
      // store this token to local storage
      localStorage.setItem("token", token);
      state.token = token;
    },
    ADD_USER: (state, username) => {
      // store the username in localstorage
      localStorage.setItem("username", username);
      state.username = username;
    },
    REMOVE_TOKEN_AND_USER: state => {
      // remove the record in local storage
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      // remove the vuex record
      state.token = "";
      state.username = "";
      // remove the axios record
      axios.defaults.headers.common["Authorization"] = null;
    }
  },
  actions: {
    async loginByCredential({ commit, state }, credential) {
      const res = await axios.post("jwt/", credential);
      // add this token to store
      // modify the auth type
      commit("ADD_TOKEN", "JWT " + res.data.token);
      commit("ADD_USER", credential.username);
      // use this token to do axios request
      axios.defaults.headers.common["Authorization"] = state.token;
      // return back this promise back to support chaining
      return res;
    },
    async registerByUser({ dispatch }, user) {
      await axios.post("users/", user);
      dispatch("loginByCredential", {
        username: user.username,
        password: user.password
      });
    },
    async editUser({ commit }, user) {
      commit("API_WAITING");
      let ret = await axios.put(`users/${user.id}/`, user);
      commit("API_FINISHED");
      return ret;
    },
    async getUserDetail({ commit }) {
      commit("API_WAITING");
      let ret = await axios.get("users/");
      commit("API_FINISHED");
      return ret;
    },
    logout({ commit }) {
      // remove the record in vuex
      commit("REMOVE_TOKEN_AND_USER");
    }
  }
};
