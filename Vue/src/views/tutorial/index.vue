<!--
Developers: Jason Liu and Damian Rene
-->

<template>
  <v-container fluid style="height: calc(100vh - 64px); overflow: auto">
    <v-container>
      <v-stepper class="ma-8" v-model="step">
        <v-stepper-header>
          <template v-for="group in groups">
            <v-divider
              v-if="group.step > 1"
              :key="`${group.step}-divider`"
            ></v-divider>
            <v-stepper-step :key="group.step" :step="group.step" editable>
              {{ group.name }}
            </v-stepper-step>
          </template>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content
            v-for="group in groups"
            :key="group.step"
            :step="group.step"
          >
            <v-card class="ma-2 rounded-xl" elevation="4">
              <v-carousel height="50vh" show-arrows-on-hover>
                <v-carousel-item v-for="(el, i) in group.els" :key="i">
                  <v-img
                    height="50vh"
                    contain
                    :src="require(`@/assets/tutorial_images/${el}.jpg`)"
                  ></v-img>
                </v-carousel-item>
              </v-carousel>
            </v-card>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
      <v-btn class="mx-8" color="primary" @click="$router.go(-1)">
        Return
      </v-btn>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: "Tutorial",
  data() {
    return {
      step: 1,
      groups: [
        {
          name: "Basics",
          step: 1,
          els: ["Leaderboard", "Profile", "Workspace", "Question"],
        },
        {
          name: "Widgets",
          step: 2,
          els: [
            "Timer",
            "Buzzer",
            "Guesses",
            "Pronunciation",
            "Country",
            "Similarity",
          ],
        },
        {
          name: "Workspaces",
          step: 3,
          els: ["Workspace title", "Workspace settings", "Workspace options"],
        },
      ],
    };
  },
  methods: {
    go_back(){
      this.$router.go(-1);
  }
  }
};
</script>