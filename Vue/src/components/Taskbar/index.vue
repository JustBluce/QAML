<!--
Developers: Jason Liu
-->

<template>
  <v-toolbar elevation="4">
    <v-toolbar-title>{{ title }}</v-toolbar-title>

<<<<<<< HEAD
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
=======
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
>>>>>>> origin/Login-Features

    <v-btn
      v-if="qa"
      color="red"
      class="mx-2"
      text
      outlined
      @click="
        $store.state.workspaces.forEach((workspace) =>
          $store.commit('removeWorkspace', workspace.id)
        )
      "
    >
      Clear all
    </v-btn>

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