<!--
Developers: Jason Liu
-->

<template>
  <vue-resizable
    class="resizable-container"
    :left="style.left"
    :top="style.top"
    :width="style.width"
    :height="style.height"
    :max-width="maxW"
    :max-height="maxH"
    :min-width="minW"
    :min-height="minH"
    :fit-parent="true"
    dragSelector=".drag-selector"
    @resize:move="eHandler"
    @resize:start="eHandler"
    @resize:end="eHandler"
    @drag:move="eHandler"
    @drag:start="eHandler"
    @drag:end="eHandler"
  >
    <v-card
      ref="workspaceContainer"
      class="workspace-container"
      :style="{
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
      <Titlebar :id="id" @maximize="maximize" />

      <v-sheet class="ui-wrapper">
        <v-sheet class="ui-container">
          <WidgetContainer :id="id" container="left" />
          <QA :id="id" />
          <WidgetContainer :id="id" container="right" />
        </v-sheet>
      </v-sheet>

      <Results :id="id" />
    </v-card>
  </vue-resizable>
</template>

<script>
import Titlebar from "./Titlebar";
import WidgetContainer from "@/components/Widget/WidgetContainer";
import QA from "@/components/QA";
import Results from "@/components/Results";
import VueResizable from "vue-resizable";

export default {
  name: "Workspace",
  props: {
    id: Number,
  },
  data() {
    return {
      maxW: undefined,
      maxH: undefined,
      minW: 1024,
      minH: 64,
    };
  },
  components: {
    Titlebar,
    WidgetContainer,
    QA,
    Results,
    VueResizable,
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
      return this.$parent.$parent.$el;
    },
    eHandler(data) {
      this.style.left = data.left;
      this.style.top = data.top;
      this.style.width = data.width;
      this.style.height = data.height;
    },
    maximize() {
      this.style.top = 0;
      this.style.left = 0;
      this.style.width = this.app().offsetWidth - 16;
      this.style.height = this.app().offsetHeight - 116;
    },
    bounds() {
      this.maxW = this.app().offsetWidth - 16;
      this.maxH = this.app().offsetHeight - 116;
      this.style.width = Math.min(this.style.width, this.maxW);
      this.style.height = Math.min(this.style.height, this.maxH);
    },
  },
  mounted() {
    this.bounds();
    if (this.style.width === 0 || this.style.height === 0) {
      this.maximize();
    }
    this.interval = setInterval(this.bounds, 100);
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
};
</script>

<style scoped>
.resizable-container {
  position: absolute;
  margin: 8px;
}

.workspace-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
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
