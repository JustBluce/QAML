<!--
Developers: Jason Liu
-->

<template>
  <v-card class="mb-3" min-width="350">
    <v-card-title class="widget-title">
      {{ widget.title }}
      <v-spacer></v-spacer>
      <v-btn icon @click="deleteWidget">
        <v-icon color="close">mdi-close-circle</v-icon>
      </v-btn>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <component
        :is="widget.type"
        :workspace_id="workspace_id"
        :widget_id="widget.id"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import Vue from "vue";

const UIs = require.context("./UI", true, /\.vue$/i);
UIs.keys().forEach((path) => {
  Vue.component(UIs(path).default.name, UIs(path).default);
});

export default {
  name: "Widget",
  props: {
    workspace_id: Number,
    widget: Object,
  },
  methods: {
    deleteWidget() {
      this.$store.commit("deleteWidget", {
        workspace_id: this.workspace_id,
        widget_id: this.widget.id,
      });
    },
  },
};
</script>

<style scoped>
.widget-title {
  cursor: grab;
}
</style>