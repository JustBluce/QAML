<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <draggable
    v-model="widgets"
    ghost-class="ghost"
    handle=".handle"
    group="widgets"
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
  },
};
</script>

<style scoped>
.widget-item {
  margin-top: 20px;
  margin-left: 20px;
}

.widgets-move {
  transition: all 0.3s ease;
}

.widgets-enter-active,
.widgets-leave-active {
  transition: all 0.3s ease;
  position: absolute;
}

.widgets-enter,
.widgets-leave-to {
  opacity: 0;
}

.ghost {
  opacity: 0.3;
}
</style>
