<!--
Developers: Jason Liu
-->

<template>
  <v-tabs
    v-model="workspace_selected"
    ref="tabs"
    background-color="background"
    show-arrows
    height="36"
  >
    <v-tab v-show="false"></v-tab>
    <draggable class="ma-0 row" v-model="workspaces">
      <v-tab
        v-show="workspace.tab"
        v-for="workspace in workspaces"
        :key="workspace.tab_id"
        :ref="`tab-${workspace.id}`"
        :ripple="false"
        @click="
          if (workspace.tab) $store.commit('selectWorkspace', workspace.id);
        "
      >
        {{ workspace.title }}
        <v-icon
          class="ml-2"
          color="red"
          small
          @click="$store.commit('closeWorkspace', workspace.id)"
          >mdi-close</v-icon
        >
      </v-tab>
    </draggable>
  </v-tabs>
</template>

<script>
import draggable from "vuedraggable";

export default {
  name: "Tabs",
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
        let stack = this.$store.state.workspace_stack;
        if (stack.length > 0) {
          this.$refs[`tab-${stack.slice(-1)[0]}`][0].$el.click();
        }
      },
    },
  },
  mounted() {
    this.interval = setInterval(
      function () {
        this.$refs.tabs.onResize();
      }.bind(this),
      100
    );
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
};
</script>
