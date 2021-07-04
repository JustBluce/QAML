<!--
Developer: Jason Liu
-->

<template>
  <div class="widget-container">
    <div class="header">
      <a class="fas fa-bars btn handle" />
      <div class="title">{{ widget.title }}</div>
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
      <a class="fas fa-times btn" @click="deleteWidget" />
    </div>
    <div
      class="ui-container"
      :style="{
        display: !widget.expanded ? displayUI : 'block',
        maxHeight: widget.expanded ? widget.maxHeight : '0px',
        opacity: widget.expanded ? '1' : '0',
      }"
    >
      <component
        :is="widget.type"
        :workspace_id="workspace_id"
        :widget_id="widget.id"
      />
    </div>
  </div>
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
    displayUI: String,
  },
  computed: {
    title: {
      get() {
        return this.$store.getters.widget(this.workspace_id, this.widget.id)
          .title;
      },

      set(value) {
        this.$store.commit("updateWidget", {
          workspace_id: this.workspace_id,
          payload: { id: this.widget.id, title: value },
        });
      },
    },
  },
  methods: {
    toggleWidget() {
      console.log("here");
      this.$store.commit("toggleWidget", {
        workspace_id: this.workspace_id,
        widget_id: this.widget.id,
      });
    },
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
.widget-container {
  background: white;
  border: 2px solid steelblue;
  border-radius: 5px;
  padding: 20px;
  margin: 0px;
  width: 100%;
}

.header {
  display: flex;
  width: 100%;
  font-size: 20px;
  align-items: center;
}

.title {
  width: auto;
  font-weight: bold;
  flex-grow: 1;
}

.fas {
  width: 24px;
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