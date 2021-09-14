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
      border:
        workspace_selected === id
          ? `2px solid ${$vuetify.theme.currentTheme.primary}`
          : '',
      cursor: 'default',
    }"
    elevation="4"
    @mousedown="$store.commit('selectWorkspace', id)"
  >
    <Titlebar
      :id="id"
      @startDrag="startDrag($event, elementMove)"
      @maximize="maximize"
    />

    <v-sheet class="ui-wrapper">
      <v-sheet class="ui-container">
        <WidgetContainer :id="id" container="left" />
        <QA :id="id" />
        <WidgetContainer :id="id" container="right" />
      </v-sheet>
    </v-sheet>

    <v-btn
      class="mb-8"
      color="primary"
      absolute
      small
      bottom
      right
      fab
      @mousedown="startDrag($event, elementResize)"
    >
      <v-icon>mdi-arrow-top-left-bottom-right</v-icon>
    </v-btn>

    <Results :id="id"/>
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
  data() {
    return {
      clientX: undefined,
      clientY: undefined,
    };
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
    app() {
      return this.$parent.$parent.$parent.$el;
    },
    startDrag(event, func) {
      event.preventDefault();
      this.clientX = event.clientX;
      this.clientY = event.clientY;
      document.onmousemove = func;
      document.onmouseup = this.stopDrag;
    },
    elementDrag(event) {
      let movementX = this.clientX - event.clientX;
      let movementY = this.clientY - event.clientY;
      this.clientX = event.clientX;
      this.clientY = event.clientY;
      return { movementX, movementY };
    },
    elementMove(event) {
      event.preventDefault();
      let { movementX, movementY } = this.elementDrag(event);
      this.style.left = Math.min(
        this.app().offsetWidth - 100,
        Math.max(0, this.style.left - movementX)
      );
      this.style.top = Math.min(
        this.app().offsetHeight - 200,
        Math.max(0, this.style.top - movementY)
      );
      document.onmouseleave = this.stopDrag;
    },
    elementResize(event) {
      event.preventDefault();
      let { movementX, movementY } = this.elementDrag(event);
      this.style.width = Math.min(
        this.app().offsetWidth - 16,
        this.style.width - movementX
      );
      this.style.height = Math.min(
        this.app().offsetHeight - 16,
        this.style.height - movementY
      );
    },
    stopDrag() {
      document.onmousemove = null;
      document.onmouseup = null;
      document.onmouseleave = null;
      this.style.width = Math.max(1024, this.style.width);
      this.style.height = Math.max(64, this.style.height);
    },
    maximize() {
      this.style.top = 0;
      this.style.left = 0;
      this.style.width = this.app().offsetWidth - 16;
      this.style.height = this.app().offsetHeight - 16;
    },
  },
  mounted() {
    if (this.style.width === 0 || this.style.height === 0) {
      this.maximize();
    }
  },
};
</script>

<style scoped>
.workspace-container {
  display: flex;
  flex-direction: column;
  position: absolute;
  min-width: 1024px;
  max-width: calc(100% - 16px);
  min-height: 64px;
  max-height: calc(100% - 16px);
  margin: 8px;
  padding: 0;
  overflow: hidden;
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
