<template>
  <v-btn flat>{{ fullname }}</v-btn>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: () => ({
    actions: []
  }),
  computed: {
    ...mapState({
      fullname: state => state.auth.first_name + state.auth.last_name
    })
  }
};
</script>
