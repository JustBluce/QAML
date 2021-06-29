<!--
Developers: Jason Liu
-->

<template>
  <div
    class="fit workspace-container"
    :style="{ left: positions.left + 'px', top: positions.top + 'px' }"
  >
    <div class="drag-bar" @mousedown="startDrag" />
    <h2>
      <div class="dropdown">
        <a class="fas fa-chevron-circle-down btn" />
        <div class="menu">
          <div
            v-for="widget_type in widget_types"
            class="fit widget-type-item"
            :key="widget_type"
            @click="addWidget(widget_type)"
          >
            {{ widget_type }}
          </div>
        </div>
      </div>
      <input value="Workspace Demo" />
      <a class="fas fa-minus btn" @click="minimize" />
      <a class="fas fa-times btn" @click="close" />
    </h2>
    <draggable
      v-model="widgets"
      class="widgets-container"
      ghost-class="ghost"
      handle=".handle"
      group="widgets"
      :force-fallback="true"
      :scroll-sensitivity="200"
      @start="drag = true"
      @end="(drag = false), (displayUI = 'block')"
    >
      <transition-group type="transition" name="widgets">
        <div class="fit widget-item" v-for="widget in widgets" :key="widget.id">
          <Widget
            :widget="widget"
            :displayUI="displayUI"
            @mousedown.native="displayUI = 'none'"
            @mouseup.native="displayUI = 'block'"
          />
        </div>
      </transition-group>
    </draggable>
  </div>
</template>

<script>
import Widget from "@/components/Widget";
import draggable from "vuedraggable";

export default {
  components: {
    Widget,
    draggable,
  },
  data() {
    return {
      positions: {
        clientX: undefined,
        clientY: undefined,
        left: 0,
        top: 0,
      },
      drag: false,
      displayUI: "block",
    };
  },
  computed: {
    widgets: {
      get() {
        return this.$store.state.widgets;
      },

      set(widgets) {
        this.$store.state.widgets = widgets;
      },
    },
    widget_types() {
      return this.$store.state.widget_types;
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
    addWidget(type) {
      this.$store.commit("addWidget", type);
    },
    minimize() {},
    close() {},
  },
};
</script>

<style scoped>
.workspace-container {
  position: absolute;
  margin: 20px;
  border: 4px solid steelblue;
}

.drag-bar {
  cursor: move;
  height: 10px;
  background-color: steelblue;
}

h2 {
  display: flex;
  margin: 0px;
  padding: 10px;
  font-weight: normal;
}

.fas {
  width: 30px;
  text-align: right;
}

.fa-chevron-circle-down {
  text-align: left;
}

.dropdown {
  display: flex;
  flex-direction: column;
}

.menu {
  background-color: rgba(256, 256, 256, 0.98);
  overflow: hidden;
  visibility: hidden;
  max-height: 0px;
  margin-top: 24px;
  padding: 0px;
  width: auto;
  transition: max-height 0.3s, visibility 0s 0.3s linear;
  position: absolute;
}

.dropdown:hover .menu {
  visibility: visible;
  max-height: 150px;
  transition: max-height 0.3s, visibility 0s 0s linear;
}

.widget-type-item {
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
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

.widgets-container {
  background-color: #f1f1f1;
  resize: vertical;
  overflow: auto;
  overflow: overlay;
  padding: 20px;
  padding-top: 0px;
}

.widget-item {
  margin-top: 20px;
}

.widgets-move {
  transition: all 0.3s ease;
}

.widgets-enter-active,
.widgets-leave-active {
  transition: all 0.3s ease;
}

.widgets-enter,
.widgets-leave-to {
  opacity: 0;
}

.ghost {
  opacity: 0.3;
}
</style>
