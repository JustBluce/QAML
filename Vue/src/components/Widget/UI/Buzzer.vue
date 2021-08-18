<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div>
    <v-card class="background mb-4 pa-2">
      <Highlighter
        highlightClassName="highlight"
        :searchWords="keywords"
        :autoEscape="true"
        :textToHighlight="binary_search_based_buzzer"
      />
    </v-card>
    <v-textarea
      readonly
      class="container"
      rows="1"
      v-model="buzz_guess"
    ></v-textarea>
    <v-data-table
      :headers="headers"
      :items="importance"
      hide-default-footer
      class="elevation-2"
    >
    </v-data-table>
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";

export default {
  name: "Buzzer",
  props: {
    workspace_id: Number,
  },
  components: {
    Highlighter,
  },
  data() {
    return {
      headers: [
        { text: "Sentence", value: "sentence" },
        { text: "Importance", value: "importance" },
      ],
      words: "🔔BUZZ",
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    binary_search_based_buzzer() {
      return this.qa.binary_search_based_buzzer;
    },
    importance() {
      return this.qa.importance;
    },
    buzz_guess() {
      if (this.qa.top_guess_buzzer === "") {
        return "The buzzer does not buzz";
      } else {
        return "The buzzer guess is: " + this.qa.top_guess_buzzer;
      }
    },
    keywords() {
      return this.words.split(" ");
    },
  },
};
</script>

<style scoped>
.highlight {
  background-color: #fffab8;
}
</style>