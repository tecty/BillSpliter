import axios from "axios";

export default {
  namespaced: true,
  actions: {
    get_curr_bill: () => axios.get("bills/"),
    get_base_url: (state, id, action = "") => `bills/${id}/` + action,
    b_approve(state, id) {
      return axios.get(`bills/${id}/approve/`);
    },
    b_reject: (state, id) => axios.get(`bills/${id}/reject/`),
    b_resume: (state, id) => axios.get(`bills/${id}/resume/`),
    b_approve_all: () => axios.get("bills/approve_all/")
  }
};
