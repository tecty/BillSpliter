import axios from "axios";
export default {
  namespaced: true,
  actions: {
    s_get: (state, id = "") => {
      if (id != "") {
        id = id + "/";
      }
      return axios.get(`settlement/${id}`);
    },
    s_create: (state, data) => axios.post("settlement/", data),
    s_delete: (state, id) => axios.delete(`settlement/${id}/`),
    s_get_wait_bill: (state, id) => axios.get(`settlement/${id}/waiting_bill/`),
    s_get_incl_bill: (state, id) => axios.get(`settlement/${id}/include_bill/`),
    s_get_stat: (state, id) => axios.get(`settlement/${id}/statistic/`),
    str_approve: (state, id) => axios.get(`settle_tr/${id}/approve/`),
    str_reject: (state, id) => axios.get(`settle_tr/${id}/reject/`)
  }
};
