<!--
Developers: Jason Liu
-->

<template>
  <div
    class="workspace-container"
    :style="{ left: positions.left + 'px', top: positions.top + 'px' }"
  >
    <div class="drag-bar" @mousedown="startDrag" />
    <h2>
      <div class="dropdown">
        <a class="fas fa-chevron-circle-down btn" />
        <div class="menu expandable fit">
          <a id="add-widget" class="menu-item" @click="toggleSubMenu"
            >Add Widget</a
          >
          <div :class="classSubMenu('add-widget')">
            <div
              v-for="widget_type in widget_types"
              class="sub-menu-item"
              :key="widget_type"
              @click="addWidget(widget_type)"
            >
              {{ widget_type }}
            </div>
          </div>
          <a id="load-widget" class="menu-item" @click="toggleSubMenu"
            >Load Widget</a
          >
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
            :workspace_id="id"
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
  name: "Workspace",
  props: {
    id: Number,
  },
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
      showSubMenus: {
        "add-widget": false,
        "load-widget": false,
      },
    };
  },
  computed: {
    widgets: {
      get() {
        return this.$store.getters.workspace(this.id).widgets;
      },

      set(widgets) {
        this.$store.getters.workspace(this.id).widgets = widgets;
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
    toggleSubMenu(event) {
      this.showSubMenus[event.target.id] = !this.showSubMenus[event.target.id];
    },
    classSubMenu(name) {
      return (
        "sub-menu expandable fit" +
        (this.showSubMenus[name] ? " show-sub-menu" : "")
      );
    },
    addWidget(type) {
      this.$store.commit("addWidget", { workspace_id: this.id, type: type });
    },
    minimize() {},
    close() {},
  },
};
</script>

<style scoped>
.workspace-container {
  position: absolute;
  padding: 20px;
  outline: 4px solid steelblue;
  outline-offset: -20px;
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

.menu {
  display: flex;
  flex-direction: column;
  background-color: rgba(256, 256, 256, 0.98);
  border: 2px solid steelblue;
  border-radius: 4px;
  padding: 0px;
  position: absolute;
}

.menu-item {
  font-size: 18px;
  cursor: pointer;
  padding: 6px;
  box-sizing: border-box;
}

.menu-item:hover {
  background-color: rgba(248, 248, 248, 0.98);
}

.sub-menu {
  background-color: rgba(241, 241, 241, 0.98);
  width: auto;
}

.sub-menu-item {
  font-size: 14px;
  cursor: pointer;
  padding: 6px;
  padding-top: 2px;
  padding-bottom: 2px;
  transition: background-color 0.3s;
}

.sub-menu-item:hover {
  background-color: rgba(234, 234, 234, 0.98);
}

.expandable {
  overflow: hidden;
  visibility: hidden;
  max-height: 0px;
  transition: max-height 0.3s, visibility 0s 0.3s linear;
}

.dropdown:hover .menu,
.show-sub-menu {
  visibility: visible;
  max-height: 150px;
  transition: max-height 0.3s, visibility 0s 0s linear;
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
  height: 500px;
  max-height: 1000px;
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
