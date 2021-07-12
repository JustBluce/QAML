<!--
Developers: Jason Liu
-->

<template>
  <div
    class="workspace-container"
    :style="{
      left: style.left + 'px',
      top: style.top + 'px',
      zIndex: zIndex,
      filter: workspace_selected === id ? 'contrast(100%)' : 'contrast(85%)',
    }"
    @mousedown="onSelect"
  >
    <div class="drag-bar" @mousedown="startDrag" />
    <Header :workspace_id="id" />
    <div class="ui-wrapper">
      <div class="ui-container">
        <WidgetContainer :workspace_id="id" container="left" />
        <QA :workspace_id="id" :qa_id="qa_selected" />
        <WidgetContainer :workspace_id="id" container="right" />
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./Header";
import WidgetContainer from "./WidgetContainer";
import QA from "./QA";

export default {
  name: "Workspace",
  props: {
    id: Number,
  },
  components: {
    Header,
    WidgetContainer,
    QA,
  },
  data() {
    return {
      clientX: undefined,
      clientY: undefined,
    };
  },
  computed: {
    widget_types() {
      return this.$store.state.widget_types;
    },
    workspace() {
      return this.$store.getters.workspace(this.id);
    },
    style() {
      return this.workspace.style;
    },
    qa_selected() {
      return this.workspace.qa_selected;
    },
    workspace_selected() {
      return this.$store.state.workspace_stack.slice(-1)[0];
    },
    zIndex() {
      return this.$store.state.workspace_stack.indexOf(this.id);
    },
  },
  methods: {
    startDrag(event) {
      event.preventDefault();
      this.clientX = event.clientX;
      this.clientY = event.clientY;
      document.onmousemove = this.elementDrag;
      document.onmouseup = this.stopDrag;
    },
    elementDrag(event) {
      event.preventDefault();
      let movementX = this.clientX - event.clientX;
      let movementY = this.clientY - event.clientY;
      this.clientX = event.clientX;
      this.clientY = event.clientY;
      this.style.left = Math.min(
        window.innerWidth - 100,
        Math.max(0, this.style.left - movementX)
      );
      this.style.top = Math.min(
        window.innerHeight - 150,
        Math.max(0, this.style.top - movementY)
      );
    },
    stopDrag() {
      document.onmousemove = null;
      document.onmouseup = null;
    },
    onSelect() {
      this.$store.commit("selectWorkspace", this.id);
    },
  },
};
</script>

<style scoped>
.workspace-container {
  display: flex;
  flex-direction: column;
  position: absolute;
  margin: 4px;
  background-color: white;
  border: 4px solid steelblue;
  box-shadow: 0px 0px 4px black;
  height: 750px;
  min-height: 750px;
  max-height: calc(100% - 8px);
  width: calc(100% - 8px);
  min-width: 1100px;
  max-width: calc(100% - 8px);
  overflow: hidden;
  resize: both;
}

.drag-bar {
  cursor: move;
  height: 10px;
  background-color: steelblue;
  flex-shrink: 0;
}

.ui-wrapper {
  flex-grow: 1;
  overflow-x: hidden;
  overflow-y: auto;
  overflow-y: overlay;
}

.ui-container {
  display: flex;
  position: relative;
  min-height: 100%;
  max-height: fit-content;
}
</style>
