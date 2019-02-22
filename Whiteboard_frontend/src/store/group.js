import axios from "axios";

export default {
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
    async refresh_grouplist({ state, commit }) {
      if (state.groupList.length == 0) {
        const res = await axios.get("groups/");
        commit("SET_GROUP_LIST", res.data.results);
        return res;
      }
      return Promise().resolve();
    }
  }
};
