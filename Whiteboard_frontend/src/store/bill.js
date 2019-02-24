import axios from "axios";

export default {
  namespaced: true,
  actions: {
    get_curr_bill: () => axios.get("bills")
  }
};
