<!--
Developers: Jason Liu
-->

<template>
  <div>
    <v-toolbar elevation="4">
      <v-toolbar-title>{{ title }}</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        v-if="qa"
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

      <Profile />

      <template v-slot:extension v-if="qa">
        <Tabs />
      </template>
    </v-toolbar>
  </div>
</template>

<script>
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