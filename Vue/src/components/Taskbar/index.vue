<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar
    :style="{ height: qa ? '90px' : '', 'z-index': 100 }"
    elevation="2"
  >
    <v-toolbar-title style="font-size: 24px">{{ title }}</v-toolbar-title>

    <v-spacer></v-spacer>

    <WorkspaceBtns v-if="qa" />

    <v-divider v-if="qa" class="my-1" vertical></v-divider>

        <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          large
          class="mr-1"
          v-bind="attrs"
          v-on="on"
          @click="$router.push('tutorial').catch(() => {})"
        >
          <v-icon>mdi-school-outline</v-icon>
        </v-btn>
      </template>
      <span>Tutorial</span>
    </v-tooltip>


    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          large
          class="mr-1"
          v-bind="attrs"
          v-on="on"
          @click="$vuetify.theme.dark = !$vuetify.theme.dark"
        >
          <v-icon>mdi-brightness-6</v-icon>
        </v-btn>
      </template>
      <span v-if="$vuetify.theme.dark">Light mode</span>
      <span v-else>Dark mode</span>
    </v-tooltip>

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