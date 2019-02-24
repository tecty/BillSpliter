<template>
  <v-container>
    <h1>Create Bill</h1>
    <v-layout row wrap>
      <GroupSelector v-model="groupId" />
      {{ groupId }}
    </v-layout>
  </v-container>
</template>
<script>
import GroupSelector from "@/components/group/Selector.vue";
export default {
  data() {
    return {
      groupId: 2
    };
  },
  components: {
    GroupSelector
  }
};
</script>
