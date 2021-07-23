<!--
Developers: Jason Liu
-->

<template>
  <v-card class="widget mb-3" elevation="4">
    <v-card-title class="widget-title">
      {{ widget.title }}
      <v-spacer></v-spacer>
      <v-btn icon @click="deleteWidget">
        <v-icon color="red">mdi-close</v-icon>
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
.widget {
  border-radius: 15px;
}

.widget-title {
  cursor: grab;
}
</style>