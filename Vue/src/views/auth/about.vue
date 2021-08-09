<!--
Developers: Jason Liu
-->

<template>
  <v-container fluid style="height: calc(100vh - 64px); overflow: auto">
    <particles-bg :color="$vuetify.theme.currentTheme.primary" type="cobweb" />

    <v-card class="mx-auto" width="80%">
      <v-card-text class="text-h4 text-center font-weight-bold">
        Adversarial Trivia Question Writing Interface
      </v-card-text>
    </v-card>
    <v-card class="pa-4 ma-16 mr-auto" width="60%" elevation="6">
      <v-card-title>Cybernetic question writing</v-card-title>
      <v-card-text class="text-body-1">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </v-card-text>
    </v-card>
    <v-card class="pa-4 ma-16 ml-auto" width="60%" elevation="6">
      <v-card-title>AI-enhanced gameplay</v-card-title>
      <v-card-text class="text-body-1">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </v-card-text>
    </v-card>
    <v-card class="pa-4 ma-16 mr-auto" width="60%" elevation="6">
      <v-card-title>Meet the team</v-card-title>
      <v-card-text class="text-body-1">
        <strong>Developers:</strong>
        Zefan Cai, Atith Gandhi, Jason Liu, Damian Rene, Raj Shah<br />
        <strong>Mentors:</strong>
        Saptarashmi Bandyopadhyay, Jordan Boyd-Graber
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { ParticlesBg } from "particles-bg-vue";

export default {
  name: "About",
  components: {
    ParticlesBg,
  },
};
</script>

<style>
</style>