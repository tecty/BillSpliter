import axios from "axios";

export default {
  namespaced: true,

  state: {},
  actions: {
    async get_curr_bill() {
      return await axios.get("bills/");
    }
  }
};
