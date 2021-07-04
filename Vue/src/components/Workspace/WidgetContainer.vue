<template>
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
      <div class="widget-item" v-for="widget in widgets" :key="widget.id">
        <Widget
          :workspace_id="workspace_id"
          :widget="widget"
          :displayUI="displayUI"
          @mousedown.native="displayUI = 'none'"
          @mouseup.native="displayUI = 'block'"
        />
      </div>
    </transition-group>
  </draggable>
</template>

<script>
import Widget from "@/components/Widget";
import draggable from "vuedraggable";

export default {
  name: "WidgetContainer",
  props: {
    workspace_id: Number,
  },
  components: {
    Widget,
    draggable,
  },
  data() {
    return {
      drag: false,
      displayUI: "block",
    };
  },
  computed: {
    widgets: {
      get() {
        return this.$store.getters.workspace(this.workspace_id).widgets;
      },

      set(widgets) {
        this.$store.getters.workspace(this.workspace_id).widgets = widgets;
      },
    },
  },
};
</script>

<style scoped>
.widgets-container {
  background-color: #f1f1f1;
  height: max(500px, 100%);
  max-height: 1000px;
  padding: 20px;
  padding-right: 5px;
  padding-top: 0px;
  overflow-y: scroll;
  resize: horizontal;
  min-width: 30%;
  max-width: 70%;
  border-right: 2px solid steelblue;
  flex-grow: -1;
}

.widget-item {
  margin: 0px;
  margin-top: 20px;
  width: 100%;
}

.widgets-move,
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