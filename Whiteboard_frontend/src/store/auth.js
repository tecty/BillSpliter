import axios from "axios";
import { getUsername, getFirstname, getLastname } from "../utils/auth";
import Router from "vue-router";

function initial() {
  return {
    id: localStorage.getItem("uid"),
    username: getUsername(),
    first_name: getFirstname(),
    last_name: getLastname()
  };
}

export default {
  namespaced: true,
  state: initial,
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
      localStorage.setItem("uid", id);
      state.username = username;
      state.first_name = first_name;
      state.last_name = last_name;
      state.id = id;
    },
    REMOVE_TOKEN_AND_USER: state => {
      // remove the record in local storage

      // remove the vuex record
      state.token = "";
      state.username = "";
    },
    RESET: state => {
      // remove all the state in localstorage
      localStorage.clear();
      // remove the axios record
      axios.defaults.headers.common["Authorization"] = null;
      const s = initial();
      Object.keys(s).forEach(key => {
        state[key] = s[key];
      });
    }
  },
  actions: {
    async loginByCredential({ commit, state, dispatch }, credential) {
      let res;
      try {
        res = await axios.post("jwt/", credential);
        // add this token to store
        // modify the auth type
        commit("ADD_TOKEN", "JWT " + res.data.token);
        localStorage.setItem("password", credential.password);
        // commit("ADD_USER", credential.username);
        // use this token to do axios request
        axios.defaults.headers.common["Authorization"] = state.token;
        // refresh token by this method
        setTimeout(() => {
          dispatch("auth/loginByCredential", credential);
        }, 270000);
      } catch (error) {
        // logout
        dispatch("clear_out");
        Router.push("/login");
      }

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
    async editUser(state, user) {
      let ret = await axios.put(`users/${user.id}/`, user);
      return ret;
    },
    async getUserDetail({ commit }) {
      let ret = await axios.get("users/");
      commit("ADD_USER", ret.data);
      return ret;
    }
  }
};
