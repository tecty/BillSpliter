import axios from "axios";
import { getUsername, getFirstname, getLastname } from "../utils/auth";

export default {
  state: {
    id: "",
    username: getUsername,
    first_name: getFirstname(),
    last_name: getLastname()
  },
  mutations: {
    ADD_TOKEN: (state, token) => {
      // store this token to local storage
      localStorage.setItem("token", token);
      state.token = token;
    },
    ADD_USER: (state, { username, first_name, last_name, id }) => {
      // store the username in localstorage
      localStorage.setItem("username", username);
      localStorage.setItem("first_name", first_name);
      localStorage.setItem("last_name", last_name);
      state.username = username;
      state.first_name = first_name;
      state.last_name = last_name;
      state.id = id;
    },
    REMOVE_TOKEN_AND_USER: state => {
      // remove the record in local storage
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("password");
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
      localStorage.setItem("password", credential.password);
      // commit("ADD_USER", credential.username);
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
      commit("ADD_USER", ret.data);
      commit("API_FINISHED");
      return ret;
    },
    logout({ commit }) {
      // remove the record in vuex
      commit("REMOVE_TOKEN_AND_USER");
    }
  }
};
