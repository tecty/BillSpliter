import axios from "axios";

export default {
  namespaced: true,
  state: {
    groupList: []
  },
  mutations: {
    SET_GROUP_LIST: (state, group_list) => {
      group_list.forEach(el => {
        if (el.users.length == 0) {
          el.name_list = "No user in this group.";
        } else {
          el.name_list =
            el.users
              .map(el => {
                if (el.first_name) return `${el.first_name} ${el.last_name}`;
                else return el.username;
              })
              .join(", ") + ".";
        }
      });
      state.groupList = group_list;
    },
    RESET: state => (state.groupList = [])
  },
  actions: {
    async require_grouplist({ state, commit }) {
      if (state.groupList.length == 0) {
        const res = await axios.get("groups/");
        commit("SET_GROUP_LIST", res.data);
        return res;
      }
      return new Promise().resolve();
    },
    g_get_group(state, id) {
      return axios.get(`groups/${id}`);
    },
    g_add_user(state, data) {
      return axios.post(`groups/${data.gid}/add_user/`, { user: data.uid });
    }
  }
};
