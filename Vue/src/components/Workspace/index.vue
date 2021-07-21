<!--
Developers: Jason Liu
-->

<template>
  <v-card
    ref="workspaceContainer"
    class="workspace-container"
    :style="{
      left: style.left + 'px',
      top: style.top + 'px',
      width: style.width + 'px',
      height: style.height + 'px',
      zIndex: zIndex,
      filter: workspace_selected === id ? 'contrast(100%)' : 'contrast(50%)',
      border:
        workspace_selected === id
          ? `2px solid ${$vuetify.theme.currentTheme.primary}`
          : '',
    }"
    @mousedown="onSelect"
    @mouseup="onRelease"
    @mouseleave="onRelease"
  >
    <Titlebar :workspace_id="id" />
    <v-sheet class="ui-wrapper">
      <v-sheet class="ui-container">
        <WidgetContainer :workspace_id="id" container="left" />
        <QA :workspace_id="id" />
        <WidgetContainer :workspace_id="id" container="right" />
      </v-sheet>
    </v-sheet>

    <Results />
  </v-card>
</template>

<script>
import Titlebar from "./Titlebar";
import WidgetContainer from "@/components/Widget/WidgetContainer";
import QA from "@/components/QA";
import Results from "@/components/Results";

export default {
  name: "Workspace",
  props: {
    id: Number,
  },
  components: {
    Titlebar,
    WidgetContainer,
    QA,
    Results,
  },
  computed: {
    style() {
      return this.$store.getters.workspace(this.id).style;
    },
    workspace_selected() {
      return this.$store.state.workspace_stack.slice(-1)[0];
    },
    zIndex() {
      return this.$store.state.workspace_stack.indexOf(this.id);
    },
  },
  methods: {
    onSelect() {
      this.$store.commit("selectWorkspace", this.id);
    },
    onRelease() {
      let workspace = this.$refs.workspaceContainer.$el;
      this.style.width = workspace.offsetWidth;
      this.style.height = workspace.offsetHeight;
    },
  },
};
</script>

<style scoped>
.workspace-container {
  display: flex;
  flex-direction: column;
  position: absolute;
  min-height: 450px;
  max-height: 100%;
  min-width: 1200px;
  max-width: 100%;
  padding: 0;
  overflow: hidden;
  resize: both;
}

.ui-wrapper {
  flex-grow: 1;
  overflow-x: hidden;
  overflow-y: auto;
}

.ui-container {
  display: flex;
  position: relative;
  min-height: 100%;
  max-height: fit-content;
}
</style>
