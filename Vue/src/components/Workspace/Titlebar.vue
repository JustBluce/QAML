<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar style="flex-grow: 0; z-index: 1">
    <v-btn
      icon
      x-large
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
          @click="
            $store.commit('addWidget', {
              workspace_id: id,
              type: widget_type,
            })
          "
        >
          <v-list-item-title>{{ widget_type }}</v-list-item-title>
        </v-list-item>
        <v-list-item v-show="widget_types.length == 0" @click="menu = false">
          <v-list-item-title>No widgets to add</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-btn icon @click="$store.commit('minimizeWorkspace', id)">
      <v-icon>mdi-window-minimize</v-icon>
    </v-btn>

    <v-btn icon @click="$emit('maximize')">
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
      menu: false,
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
      let added_types = this.workspace.widgets.map((widget) => widget.type);
      return this.$store.state.widget_types.filter(
        (type) => !added_types.includes(type)
      );
    },
  },
};
</script>