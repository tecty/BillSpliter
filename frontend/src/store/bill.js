export default {
  namespaced: true,
  actions: {
    get_curr_bill: () => window.axios.get("bills/current/"),
    get_base_url: (state, id, action = "") => `bills/${id}/` + action,
    b_approve(state, id) {
      return window.axios.get(`bills/${id}/approve/`);
    },
    b_reject: (state, id) => window.axios.get(`bills/${id}/reject/`),
    b_resume: (state, id) => window.axios.get(`bills/${id}/resume/`),
    b_approve_all: () => window.axios.get("bills/approve_all/")
  }
};
