<!--
Developers: Jason Liu and Damian Rene
-->

<template>
  <v-container fluid style="height: calc(100vh - 64px); overflow: auto;">
    <v-stepper class="ma-8" v-model="step">
      <v-stepper-header>
        <v-stepper-step :complete="step > 1" step="1">
          Name of step 1
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="step > 2" step="2">
          Name of step 2
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3"> Name of step 3 </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card class="mb-12">
            <v-img
              src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
          </v-card>

          <v-btn color="primary" @click="step = 2"> Continue </v-btn>

          <v-btn text> Cancel </v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-card class="mb-12">
            <v-img
              src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
          </v-card>

          <v-btn color="primary" @click="step = 3"> Continue </v-btn>

          <v-btn text> Cancel </v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-card class="mb-12">
            <v-img
              src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
          </v-card>

          <v-btn color="primary" @click="step = 1"> Continue </v-btn>

          <v-btn text> Cancel </v-btn>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script>
export default {
  name: "Tutorial",
  data() {
    return {
      step: 1,
    };
  },
};
</script>