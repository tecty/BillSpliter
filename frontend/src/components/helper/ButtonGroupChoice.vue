<template>
  <v-bottom-sheet v-model="_group_choice">
    <v-list>
      <v-subheader>Open in</v-subheader>
      <v-list-tile
        v-for="tile in tiles"
        :key="tile.title"
        @click="sheet = false"
      >
        <v-list-tile-avatar>
          <v-avatar size="32px" tile>
            <img
              :src="
                `https://cdn.vuetifyjs.com/images/bottom-sheets/${tile.img}`
              "
              :alt="tile.title"
            />
          </v-avatar>
        </v-list-tile-avatar>
        <v-list-tile-title>{{ tile.title }}</v-list-tile-title>
      </v-list-tile>
    </v-list>
  </v-bottom-sheet>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      tiles: [
        { img: "keep.png", title: "Keep" },
        { img: "inbox.png", title: "Inbox" },
        { img: "hangouts.png", title: "Hangouts" },
        { img: "messenger.png", title: "Messenger" },
        { img: "google.png", title: "Google+" }
      ]
    };
  },

  methods: {
    ...mapMutations("group", ["TOGGLE_CHOICE_LIST"])
  },
  computed: {
    ...mapState("group", ["group_choice"]),
    _group_choice: {
      get() {
        return this.group_choice;
      },
      set() {
        // call the mutation to close the list
        return this.TOGGLE_CHOICE_LIST();
      }
    }
  }
};
</script>
