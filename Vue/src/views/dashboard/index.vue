<template>
  <v-main>
    <Taskbar title="Dashboard" />
    <v-container fluid style="height: calc(100vh - 64px); overflow: auto">
      <v-card class="mx-lg-auto" width="50%">
        <v-card-text class="text-h3 text-center font-weight-bold">
          Adversarial Trivia Question Writing Interface
        </v-card-text>
      </v-card>
      <v-card class="pa-4 ma-16 mr-lg-auto" width="60%" elevation="6">
        <v-card-title>Cybernetic question writing</v-card-title>
        <v-card-text class="text-h6 font-weight-bold">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </v-card-text>
      </v-card>
      <v-card class="pa-4 ma-16 ml-lg-auto" width="60%" elevation="6">
        <v-card-title>AI-enhanced gameplay</v-card-title>
        <v-card-text class="text-h6 font-weight-bold">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </v-card-text>
      </v-card>
      <v-card class="pa-4 ma-16 mr-lg-auto" width="60%" elevation="6">
        <v-card-title>Meet the team</v-card-title>
        <v-card-text class="text-h6 font-weight-bold">
          Developers: Zefan Cai, Atith Gandhi, Jason Liu, Damian Rene, Raj
          Shah<br />
          Mentors: Saptarashmi Bandyopadhyay, Jordan Boyd-Graber
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
</template>

<script>
import Taskbar from "@/components/Taskbar";

export default {
  name: "Dashboard",
  components: {
    Taskbar,
  },
};
</script>
