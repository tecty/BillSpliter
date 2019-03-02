import axios from "axios";

export default {
  namespaced: true,
  actions: {
    get_curr_bill: () => axios.get("bills"),
    get_base_url: (state, id, action = "") => `bills/${id}/` + action,
    async b_approve({ dispatch }, id) {
      return axios.get(await dispatch("get_base_url", id, "approve"));
    },
    b_reject: async ({ dispatch }, id) =>
      axios.get(await dispatch("get_base_url", id, "reject")),
    b_resume: async ({ dispatch }, id) =>
      axios.get(await dispatch("get_base_url", id, "resume"))
  }
};
