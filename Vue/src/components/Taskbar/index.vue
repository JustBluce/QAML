<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar elevation="4">
    <v-toolbar-title>{{ title }}</v-toolbar-title>

    <v-spacer></v-spacer>

    <WorkspaceMenu v-if="qa" />

    <v-btn icon @click="$vuetify.theme.dark = !$vuetify.theme.dark">
      <v-icon>mdi-brightness-6</v-icon>
    </v-btn>

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