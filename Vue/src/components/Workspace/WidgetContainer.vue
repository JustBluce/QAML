<!--
Developers: Jason Liu
-->

<template>
  <draggable
    v-model="widgets"
    class="widgets-container"
    ghost-class="ghost"
    handle=".handle"
    group="widgets"
    :emptyInsertThreshold="500"
    @start="drag = true"
    @end="(drag = false), (displayUI = 'block')"
    @add="(event) => (event.item.style.display = 'none')"
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
    container: String,
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
    workspace() {
      return this.$store.getters.workspace(this.workspace_id);
    },

    widgets: {
      get() {
        return this.workspace.widgets.filter(
          (widgets) => widgets.container === this.container
        );
      },

      set(widgets) {
        this.workspace.widgets = this.workspace.widgets.filter((widget) =>
          widgets.every((container_widget) => container_widget.id !== widget.id)
        );
        widgets.map((widget) =>
          this.workspace.widgets.push({ ...widget, container: this.container })
        );
      },
    },
  },
};
</script>

<style scoped>
.widgets-container {
  background-color: #f1f1f1;
  padding: 10px;
  padding-top: 0px;
  width: 350px;
  min-width: 350px;
}

.widget-item {
  margin: 0px;
  margin-top: 20px;
  height: fit-content;
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