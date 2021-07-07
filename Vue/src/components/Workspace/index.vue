<!--
Developers: Jason Liu
-->

<template>
  <div
    class="workspace-container"
    :style="{ left: positions.left + 'px', top: positions.top + 'px' }"
  >
    <div class="drag-bar" @mousedown="startDrag" />
    <Header :workspace_id="id" />
    <div class="ui-container">
      <WidgetContainer :workspace_id="id" />
      <QA :workspace_id="id" :qa_id="qa_selected" />
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
      positions: {
        clientX: undefined,
        clientY: undefined,
        left: 0,
        top: 0,
      },
    };
  },
  computed: {
    widget_types() {
      return this.$store.state.widget_types;
    },
    qa_selected() {
      return this.$store.getters.workspace(this.id).qa_selected;
    },
  },
  methods: {
    startDrag(event) {
      event.preventDefault();
      this.positions.clientX = event.clientX;
      this.positions.clientY = event.clientY;
      document.onmousemove = this.elementDrag;
      document.onmouseup = this.stopDrag;
    },
    elementDrag(event) {
      event.preventDefault();
      let movementX = this.positions.clientX - event.clientX;
      let movementY = this.positions.clientY - event.clientY;
      this.positions.clientX = event.clientX;
      this.positions.clientY = event.clientY;
      this.positions.left = Math.max(0, this.positions.left - movementX);
      this.positions.top = Math.max(0, this.positions.top - movementY);
    },
    stopDrag() {
      document.onmousemove = null;
      document.onmouseup = null;
    },
  },
};
</script>

<style scoped>
.workspace-container {
  display: flex;
  flex-direction: column;
  position: absolute;
  padding: 20px;
  outline: 4px solid steelblue;
  outline-offset: -20px;
  width: 1500px;
}

.drag-bar {
  cursor: move;
  height: 10px;
  background-color: steelblue;
}

.ui-container {
  display: flex;
  height: 500px;
  max-height: 1000px;
  resize: vertical;
  overflow-y: scroll;
}

</style>
