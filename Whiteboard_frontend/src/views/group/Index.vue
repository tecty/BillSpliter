<template>
  <v-container>
    <h1>Groups<v-btn color="success">Cretae</v-btn></h1>
    <p>Search your group here</p>
    <GroupList />
  </v-container>
</template>
<script>
import GroupList from "@/components/group/List.vue";
export default {
  data() {
    return {};
  },
  components: {
    GroupList
  }
};
</script>
