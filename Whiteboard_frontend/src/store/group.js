import axios from "axios";
export default {
  state: {
    groupList: []
  },
  mutations: {
    SET_GROUP_LIST: (state, group_list) => (state.groupList = group_list),
    RESET: state => (state.groupList = [])
  },
  actions: {
    async refresh_grouplist({ state, commit }) {
      if (!state.groupList.length) {
        const res = await axios.get("groups/");
        commit("SET_GROUP_LIST", res.data.result);
        return res;
      }
      return Promise().resolve();
    }
  }
};
