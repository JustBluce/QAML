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
      filter: workspace_selected === id ? 'contrast(100%)' : 'contrast(50%)',
      border:
        workspace_selected === id
          ? `2px solid ${$vuetify.theme.currentTheme.primary}`
          : '',
    }"
    @mousedown="onSelect"
    @mouseup="onRelease"
    @mouseleave="onRelease"
  >
    <v-toolbar style="flex-grow: 0; z-index: 1">
      <v-btn icon style="cursor: grab" @mousedown="startDrag">
        <v-icon>mdi-drag</v-icon>
      </v-btn>

      <v-text-field
        placeholder="Title"
        hide-details="auto"
        style="font-size: 28px"
        :rules="rules"
        :value="workspace.title"
        @input="checkTitle"
      ></v-text-field>

      <v-spacer></v-spacer>

      <v-menu :close-on-content-click="false" v-model="menu" offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on" icon>
            <v-icon>mdi-hammer-wrench</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="widget_type in widget_types"
            :key="widget_type"
            link
            @click="addWidget(widget_type)"
          >
            <v-list-item-title>{{ widget_type }}</v-list-item-title>
          </v-list-item>
          <v-list-item v-show="widget_types.length == 0" @click="menu = false">
            <v-list-item-title>No widgets to add</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn icon @click="minimize">
        <v-icon>mdi-window-minimize</v-icon>
      </v-btn>

      <v-btn icon @click="maximize">
        <v-icon>mdi-window-maximize</v-icon>
      </v-btn>
    </v-toolbar>

    <v-sheet class="ui-wrapper">
      <v-sheet class="ui-container">
        <WidgetContainer :workspace_id="id" container="left" />
        <QA :workspace_id="id" />
        <WidgetContainer :workspace_id="id" container="right" />
      </v-sheet>
    </v-sheet>
  </v-card>
</template>

<script>
import WidgetContainer from "./WidgetContainer";
import QA from "./QA";

export default {
  name: "Workspace",
  props: {
    id: Number,
  },
  components: {
    WidgetContainer,
    QA,
  },
  data() {
    return {
      clientX: undefined,
      clientY: undefined,
      rules: [(value) => !!value || "Required."],
      menu: false,
    };
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.id);
    },
    workspace_selected() {
      return this.$store.state.workspace_stack.slice(-1)[0];
    },
    style() {
      return this.workspace.style;
    },
    zIndex() {
      return this.$store.state.workspace_stack.indexOf(this.id);
    },
    widget_types() {
      let added_types = this.workspace.widgets.map((widget) => widget.type);
      return this.$store.state.widget_types.filter(
        (type) => !added_types.includes(type)
      );
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
    onRelease() {
      let workspace = this.$refs.workspaceContainer.$el;
      this.style.width = workspace.offsetWidth;
      this.style.height = workspace.offsetHeight;
    },
    checkTitle(title) {
      if (title) {
        this.workspace.title = title;
      }
    },
    addWidget(type) {
      this.$store.commit("addWidget", {
        workspace_id: this.id,
        type: type,
      });
    },
    minimize() {
      this.$store.commit("minimizeWorkspace", this.id);
    },
    maximize() {
      let app = this.$parent.$parent.$el;
      this.style.width = app.offsetWidth;
      this.style.height = app.offsetHeight;
      this.style.top = 0;
      this.style.left = 0;
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
  min-height: 450px;
  max-height: 100%;
  min-width: 1200px;
  max-width: 100%;
  padding: 0;
  overflow: hidden;
  resize: both;
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
