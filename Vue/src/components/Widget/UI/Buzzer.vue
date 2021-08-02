<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div>
    <!-- <textarea
      readonly
      class="container"
      rows="5"
      placeholder="Buzzer"
      v-model="binary_search_based_buzzer"
    ></textarea> -->
    <Highlighter
      highlightClassName="highlight"
      :searchWords="keywords"
      :autoEscape="true"
      :textToHighlight="binary_search_based_buzzer"
    />
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