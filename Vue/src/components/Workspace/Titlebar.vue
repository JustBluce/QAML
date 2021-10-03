<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar style="flex-grow: 0; z-index: 1">
    <v-btn
      icon
      large
      class="mr-1"
      style="cursor: grab"
      @mousedown="$emit('startDrag', $event)"
    >
      <v-icon>mdi-drag</v-icon>
    </v-btn>

    <v-form ref="form">
      <v-text-field
        placeholder="Title"
        hide-details="auto"
        style="font-size: 24px"
        :rules="rules"
        :value="workspace.title"
        @input="
          (title) => {
            if ($refs.form.validate()) workspace.title = title;
          }
        "
      ></v-text-field>
    </v-form>

    <v-spacer></v-spacer>

    <v-btn :id="'toggleWidgets-'+id" icon large>
      <v-icon>mdi-hammer-wrench</v-icon>
      <v-tooltip bottom activator="#toggleWidgets">
        <span>Toggle widgets</span>
      </v-tooltip>
      <v-menu
        transition="fade-transition"
        offset-y
        rounded
        :activator="'#toggleWidgets-'+id"
        :close-on-content-click="false"
      >
        <v-list>
          <v-list-item>
            <v-btn
              color="green"
              class="mx-auto"
              style="width: 225px"
              text
              outlined
              @click="toggleAll(true)"
            >
              Activate all widgets
            </v-btn>
          </v-list-item>
          <v-list-item>
            <v-btn
              color="red"
              class="mx-auto"
              style="width: 225px"
              text
              outlined
              @click="toggleAll(false)"
            >
              Disable all widgets
            </v-btn>
          </v-list-item>
          <v-list-item v-for="widget_type in widget_types" :key="widget_type">
            <v-switch
              v-model="switches[widget_type]"
              :label="widget_type"
              :color="widget_type"
              @change="toggleSwitch(widget_type)"
              inset
              class="my-1"
              hide-details
            >
            </v-switch>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-btn>

    <v-btn
      icon
      large
      class="ml-1"
      @mouseup="$store.commit('minimizeWorkspace', id)"
    >
      <v-icon>mdi-window-minimize</v-icon>
    </v-btn>

    <v-btn icon large class="ml-1" @mouseup="$emit('maximize')">
      <v-icon>mdi-window-maximize</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
export default {
  name: "Titlebar",
  props: {
    id: Number,
  },
  data() {
    return {
      rules: [
        (v) => !!v || "Required.",
        (v) => v.length <= 32 || "Title must be less than 32 characters",
      ],
    };
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.id);
    },
    style() {
      return this.workspace.style;
    },
    widget_types() {
      return this.$store.state.widget_types;
    },
    switches() {
      let switches = {};
      this.widget_types.forEach(
        (type) =>
          (switches[type] = Boolean(
            this.workspace.widgets.find((widget) => widget.type === type)
          ))
      );
      return switches;
    },
  },
  methods: {
    toggleSwitch(type) {
      if (this.switches[type]) {
        this.$store.commit("addWidget", {
          workspace_id: this.id,
          type: type,
        });
      } else {
        this.$store.commit("deleteWidget", {
          workspace_id: this.id,
          type: type,
        });
      }
    },
    toggleAll(mode) {
      this.widget_types.forEach((type) => {
        this.switches[type] = mode;
        this.toggleSwitch(type);
      });
    },
  },
};
</script>