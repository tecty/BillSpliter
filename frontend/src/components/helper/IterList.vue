<template>
  <v-list class="grey lighten-4 grey--text  text--darken-1">
    <template v-for="item in items">
      <v-list-group
        v-if="item.items"
        :key="item.title"
        v-model="item.active"
        :prepend-icon="item.icon"
        no-action
      >
        <template v-slot:activator @click.prevent="menu = true">
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>

        <v-list-tile
          v-for="subItem in item.items"
          :to="subItem.href ? { name: subItem.href } : null"
          :key="subItem.title"
        >
          <v-list-tile-content>
            <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-icon>{{ subItem.icon }}</v-icon>
          </v-list-tile-action>
        </v-list-tile>
      </v-list-group>
      <v-list-group
        :key="item.action"
        v-else-if="item.group_choice"
        prepend-icon="group"
      >
        <!-- this is only for the choice of groups  -->
        <template v-slot:activator @click.prevent="menu = true">
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>Change Group</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
        <p v-for="g in groupList" :key="g.id">{{ g.name }}</p>
      </v-list-group>
      <v-list-tile
        :key="item.action"
        v-else
        :to="item.href ? { name: item.href } : null"
        @click="item.on"
      >
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title class="grey--text  text--darken-1">{{
            item.title
          }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </template>
  </v-list>
</template>

<script>
import { mapState } from "vuex";
export default {
  props: {
    items: Array,
    menu: Boolean
  },
  computed: {
    ...mapState("group", ["groupList"])
  }
};
</script>
