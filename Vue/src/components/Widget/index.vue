<!--
Developer: Jason Liu
-->

<template>
  <div class="widget-container">
    <h2 :style="{ width: widget.maxWidth }">
      <a class="fas fa-bars btn handle" />
      <input v-model="title" />
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
      <a
        v-show="widget.removable"
        class="fas fa-times btn"
        @click="deleteWidget"
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

const UIs = require.context("./UI", true, /\.vue$/i);
let widget_types = [];
UIs.keys().forEach((path) => {
  let widget_type = UIs(path).default.name;
  widget_types.push(widget_type);
  Vue.component(widget_type, UIs(path).default);
});

export default {
  name: "Widget",
  props: {
    widget: Object,
    displayUI: String,
  },
  computed: {
    title: {
      get() {
        return this.$store.getters.widget(this.widget.id).title;
      },

      set(value) {
        this.$store.commit("updateWidget", {
          id: this.widget.id,
          title: value,
        });
      },
    },
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
.widget-container {
  background: white;
  border: 2px solid steelblue;
  border-radius: 5px;
  padding: 20px;
  margin: 0px;
}

h2 {
  display: flex;
  margin: 0px;
}

input {
  width: auto;
  border: 0;
  font-weight: bold;
  outline: none;
  flex-grow: 1;
  text-overflow: ellipsis;
  padding: 0;
}

.fas {
  width: 30px;
  text-align: right;
}

.fa-bars {
  text-align: left;
}

.ui-container {
  overflow: hidden;
  transition: max-height 0.3s linear 0s, opacity 0.2s linear 0.1s;
}
</style>