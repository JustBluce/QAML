<!--
Developers: Jason Liu
-->

<template>
  <v-dialog v-model="results.dialog" width="500" persistent>
    <v-card>
      <v-card-title>
        Results
        <v-spacer></v-spacer>
        <v-btn icon @click="closeResults">
          <v-icon color="red">mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <v-expansion-panels accordion>
        <v-expansion-panel
          v-for="(result, index) in results.content"
          :key="index"
        >
          <v-expansion-panel-header>
            {{ result.title }}
          </v-expansion-panel-header>
          <v-expansion-panel-content class="ps-5">
            {{ result.body }}
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Results",
  computed: {
    results() {
      return this.$store.state.results;
    },
  },
  methods: {
    closeResults() {
      this.$store.commit("closeResults");
    },
  },
};
</script>