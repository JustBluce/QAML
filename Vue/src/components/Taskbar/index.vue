<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar style="z-index: 1000" elevation="4">
    <v-toolbar-title>{{ title }}</v-toolbar-title>

    <v-spacer></v-spacer>

    <WorkspaceMenu v-if="qa" />

    <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
    <v-btn 
    v-bind="attrs"
    v-on="on"
    icon 
    @click="$vuetify.theme.dark = !$vuetify.theme.dark">
      <v-icon>mdi-brightness-6</v-icon>
    </v-btn>
     </template>
    <span>Dark Mode </span>
    </v-tooltip>

    <Profile />

    <template v-slot:extension v-if="qa">
      <Tabs />
    </template>
  </v-toolbar>
</template>

<script>
import WorkspaceMenu from "./WorkspaceMenu";
import Profile from "./Profile";
import Tabs from "./Tabs";

export default {
  name: "Taskbar",
  props: {
    title: String,
    qa: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    WorkspaceMenu,
    Profile,
    Tabs,
  },
  computed: {
    recommended: {
      get() {
        return this.$store.state.recommended;
      },
      set(value) {
        this.$store.state.recommended = value;
      },
    },
  },
};
</script>