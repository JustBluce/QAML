<!--
Developers: Jason Liu
-->

<template>
  <v-card
    class="mb-3"
    style="border-radius: 16px"
    elevation="4"
    min-width="300"
  >
    <v-card-title class="handle py-2" style="font-size: 18px; cursor: grab">
      {{ widget.title }}
      <v-progress-linear
        class="my-1"
        :color="widget.type"
        rounded
        value="100"
        height="4"
      ></v-progress-linear>
    </v-card-title>
    <v-card-text>
      <component :is="widget.type" :workspace_id="workspace_id" />
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
};
</script>