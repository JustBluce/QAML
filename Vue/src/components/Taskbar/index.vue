<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar
    :style="{ height: qa ? '100px' : '', 'z-index': 1000 }"
    elevation="4"
  >
    <v-toolbar-title style="font-size: 24px">{{ title }}</v-toolbar-title>

    <v-spacer></v-spacer>

    <WorkspaceBtns v-if="qa" />

    <v-divider v-if="qa" class="mx-1" vertical></v-divider>

    <v-btn
      id="tutorial"
      icon
      large
      class="mx-1"
      @click="$router.push('tutorial').catch(() => {})"
    >
      <v-icon>mdi-school-outline</v-icon>
      <v-tooltip bottom activator="#tutorial">
        <span>Tutorial</span>
      </v-tooltip>
    </v-btn>

    <v-btn
      id="toggleTheme"
      icon
      large
      class="mr-1"
      @click="$vuetify.theme.dark = !$vuetify.theme.dark"
    >
      <v-icon>mdi-brightness-6</v-icon>
      <v-tooltip bottom activator="#toggleTheme">
        <span v-if="$vuetify.theme.dark">Light mode</span>
        <span v-else>Dark mode</span>
      </v-tooltip>
    </v-btn>

    <Profile />

    <template v-slot:extension v-if="qa">
      <Tabs />
    </template>
  </v-toolbar>
</template>

<script>
import WorkspaceBtns from "./WorkspaceBtns";
import Profile from "@/components/Profile";
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
    WorkspaceBtns,
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