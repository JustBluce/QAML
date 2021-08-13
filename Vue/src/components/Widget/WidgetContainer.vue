<!--
Developers: Jason Liu
-->

<template>
  <draggable
    v-model="widgets"
    ref="widgets"
    ghost-class="ghost"
    handle=".handle"
    :group="`widgets-${id}`"
    tag="v-container"
    fluid
    class="background"
    :style="{
      maxWidth: maxWidth + 'px',
      transition: 'max-width 0.3s',
    }"
    :emptyInsertThreshold="500"
    @add="(event) => (event.item.style.display = 'none')"
  >
    <transition-group type="transition" name="widgets">
      <template v-for="widget in widgets">
        <Widget :workspace_id="id" :widget="widget" :key="widget.id" />
      </template>
    </transition-group>
  </draggable>
</template>

<script>
import draggable from "vuedraggable";
import Widget from "@/components/Widget";

export default {
  name: "WidgetContainer",
  props: {
    id: Number,
    container: String,
  },
  components: {
    draggable,
    Widget,
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.id);
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
    maxWidth() {
      return this.widgets.length > 0 ? 350 : 50;
    },
  },
};
</script>
