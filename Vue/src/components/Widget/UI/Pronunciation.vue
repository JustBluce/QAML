<!--
Developers: Damien Rene and Jason Liu
-->

<template>
  <div>
    <!-- <div class="placeholder" v-show="!qa.text">Please enter your question</div>
    <Highlighter
      :style="{ color: 'black' }"
      highlightClassName="highlight"
      :searchWords="keywords"
      :autoEscape="true"
      :textToHighlight="qa.text"
    /> -->
    <!-- <div>
      <h4> Please add the pronunciation guide for the following words </h4>
    </div> -->
    <!-- <v-textarea
      readonly    
      color="background"
      rows="1"
      placeholder="Pronunciation highlighting"
      v-model="pronunciation"
    ></v-textarea> -->
    <h4 class="mb-2">
      Please add the pronunication guide for the following words
    </h4>
    <v-data-table
      hide-default-header
      hide-default-footer
      dense
      :headers="headers"
      :items="pronunciation"
      class="elevation-2"
    ></v-data-table>
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";
export default {
  name: "Pronunciation",
  props: {
    workspace_id: Number,
  },
  components: {
    Highlighter,
  },
  data() {
    return {
      words: "and or the quick",
      headers: [{ text: "Word", value: "Word" }],
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    pronunciation() {
      return this.qa.pronunciation;
    },
    keywords() {
      return this.words.split(" ");
    },
  },
  methods: {},
};
</script>
