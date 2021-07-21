<!--
Developers: Jason Liu
-->

<template>
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
</template>

<script>
export default {
  name: "Titlebar",
  props: {
    workspace_id: Number,
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
      return this.$store.getters.workspace(this.workspace_id);
    },
    style() {
      return this.workspace.style;
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
    checkTitle(title) {
      if (title) {
        this.workspace.title = title;
      }
    },
    addWidget(type) {
      this.$store.commit("addWidget", {
        workspace_id: this.workspace_id,
        type: type,
      });
    },
    minimize() {
      this.$store.commit("minimizeWorkspace", this.workspace_id);
    },
    maximize() {
      let app = this.$parent.$parent.$parent.$parent.$el;
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