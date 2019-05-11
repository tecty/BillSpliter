<template>
  <v-list class="grey lighten-4">
    <template v-for="(item, i) in items">
      <v-layout row v-if="item.heading" align-center :key="i">
        <v-flex xs6>
          <v-subheader v-if="item.heading">{{ item.heading }}</v-subheader>
        </v-flex>
        <v-flex xs6 class="text-xs-right" v-if="item.text">
          <v-btn
            small
            flat
            :to="item.href ? { name: item.href } : null"
            class="grey--text  text--darken-1"
            >{{ item.text }}</v-btn
          >
        </v-flex>
      </v-layout>
      <v-divider
        dark
        v-else-if="item.divider"
        class="my-3"
        :key="i"
      ></v-divider>
      <v-list-tile :key="i" v-else :to="item.href ? { name: item.href } : null">
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title class="grey--text  text--darken-1">{{
            item.text
          }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </template>
  </v-list>
</template>

<script>
export default {
  props: {
    items: Array
  }
};
</script>
