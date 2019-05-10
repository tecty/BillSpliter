export default {
  namespaced: true,
  actions: {
    s_get: (state, id = "") => {
      if (id != "") {
        id = id + "/";
      }
      return window.axios.get(`settlement/${id}`);
    },
    s_create: (state, data) => window.axios.post("settlement/", data),
    s_delete: (state, id) => window.axios.delete(`settlement/${id}/`),
    s_get_wait_bill: (state, id) =>
      window.axios.get(`settlement/${id}/waiting_bill/`),
    s_get_incl_bill: (state, id) =>
      window.axios.get(`settlement/${id}/include_bill/`),
    s_get_stat: (state, id) => window.axios.get(`settlement/${id}/statistic/`),
    str_approve: (state, id) => window.axios.get(`settle_tr/${id}/approve/`),
    str_reject: (state, id) => window.axios.get(`settle_tr/${id}/reject/`)
  }
};
