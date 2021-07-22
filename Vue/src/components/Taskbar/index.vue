<!--
Developers: Jason Liu
-->

<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>QA Interface</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        color="green"
        class="mx-2"
        text
        outlined
        @click="$store.commit('createWorkspace')"
      >
        Create workspace
      </v-btn>

      <v-btn icon @click="$vuetify.theme.dark = !$vuetify.theme.dark">
        <v-icon>mdi-brightness-6</v-icon>
      </v-btn>

      <template v-slot:extension>
        <v-tabs v-model="workspace_selected" ref="tabs" background-color="background" show-arrows>
          <v-tab v-show="false"></v-tab>
          <draggable class="ma-0 row" v-model="workspaces">
            <v-tab
              v-for="workspace in workspaces"
              :key="workspace.tab_id"
              :ripple="false"
            >
              {{ workspace.title }}
              <v-icon
                class="ml-2"
                color="red"
                small
                @click="$store.commit('removeWorkspace', workspace.id)"
                >mdi-close</v-icon
              >
            </v-tab>
          </draggable>
        </v-tabs>
      </template>
    </v-toolbar>
  </div>
</template>

<script>
import draggable from "vuedraggable";

export default {
  name: "Taskbar",
  components: {
    draggable,
  },
  computed: {
    workspaces: {
      get() {
        return this.$store.state.workspaces;
      },
      set(value) {
        this.$store.state.workspaces = value;
        this.$store.commit("updateTabs");
      },
    },
    workspace_selected: {
      get() {
        return this.$store.state.workspace_selected;
      },
      set(value) {
        this.$store.commit(
          "selectWorkspace",
          this.$store.state.workspaces.find(
            (workspace) => workspace.tab_id === value
          ).id
        );
      },
    },
    recommended: {
      get() {
        return this.$store.state.recommended;
      },
      set(value) {
        this.$store.state.recommended = value;
      },
    },
  },
  mounted() {
    let self = this;
    this.interval = setInterval(function () {
      self.$refs.tabs.onResize();
    }, 100);
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
};
</script>