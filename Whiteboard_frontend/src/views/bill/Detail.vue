<template>
  <v-container>
    <h1>
      <span class="info--text">#{{ id }}</span>
      {{ title }}
    </h1>
    <h3 class="secondary--text">{{ description }}</h3>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      id: 2,
      title: "hello",
      description: "helloworld "
    };
  },
  async mounted() {
    let ret = await axios.get(`bills/${this.$route.params.id}`);

    this.id = ret.data.id;
    this.title = ret.data.title;
    this.description = ret.data.description;
    this.transactions = ret.data.transactions;
  }
};
</script>
