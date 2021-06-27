<!--
Developer: Jason Liu
-->

<template>
  <div class="widget-container">
    <h2 :style="{ width: widget.maxWidth }">
      <a class="fas fa-bars btn handle" />
      {{ widget.title }}
      <a
        v-show="widget.removable"
        class="fas fa-times btn"
        @click="deleteWidget"
      />
      <a
        v-show="widget.expanded"
        class="fas fa-minus btn"
        @click="toggleWidget"
      />
      <a
        v-show="!widget.expanded"
        class="fas fa-plus btn"
        @click="toggleWidget"
      />
    </h2>
    <div
      class="ui-container"
      :style="{
        display: !widget.expanded ? displayUI : 'block',
        maxHeight: widget.expanded ? widget.maxHeight : '0px',
        opacity: widget.expanded ? '1' : '0',
      }"
    >
      <component :is="widget.type" :id="widget.id" />
    </div>
  </div>
</template>

<script>
import Vue from "vue";

const Widgets = require.context("./Widgets", true, /\.vue$/i);
let widget_types = [];
Widgets.keys().forEach((path) => {
  let widget_type = Widgets(path).default.name;
  widget_types.push(widget_type);
  Vue.component(widget_type, Widgets(path).default);
});

export default {
  name: "Widget",
  props: {
    widget: Object,
    displayUI: String,
  },
  methods: {
    toggleWidget() {
      this.$store.commit("toggleWidget", this.widget.id);
    },
    deleteWidget() {
      this.$store.commit("deleteWidget", this.widget.id);
    },
  },
  mounted() {
    this.$store.state.widget_types = widget_types;
  },
};
</script>

<style scoped>
h2 {
  margin: 0px;
}

.fas {
  float: right;
  margin-left: 10px;
}

.fa-bars {
  margin-left: 0px;
  margin-right: 5px;
  float: none;
}

.fa-minus,
.fa-minus:hover {
  color: #a62c2b;
}

.fa-plus,
.fa-plus:hover {
  color: #296e01;
}

.widget-container {
  background: white;
  border: 2px solid steelblue;
  border-radius: 5px;
  padding: 30px;
  margin: 0px;
}

.ui-container {
  overflow: hidden;
  transition: max-height 0.3s linear 0s, opacity 0.2s linear 0.1s;
}
</style>