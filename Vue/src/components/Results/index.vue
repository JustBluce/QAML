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
      <v-list three-line :expand="true">
        <template v-for="(result, index) in results.content">
          <div :key="index">
            <v-divider v-if="index > 0"></v-divider>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>{{ result.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ result.body }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </div>
        </template>
      </v-list>
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