<!--
Developer: Damien Rene and Jason Liu
-->

<template>
  <div>
    <div readonly class="output output-container" @click="clickMethod">
      <input
        readonly
        v-show="!text"
        class="output"
        placeholder="Please enter your question"
      />
      <Highlighter
        class="my-highlight"
        :style="{ color: 'black' }"
        highlightClassName="highlight"
        :searchWords="keywords"
        :autoEscape="true"
        :textToHighlight="text"
      />
    </div>
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";
export default {
  name: "Pronunciation",
  props: {
    question_id: String,
  },
  components: {
    Highlighter,
  },
  data() {
    return {
      words: "and or the quick",
    };
  },
  computed: {
    text: {
      get() {
        return this.$store.getters.questions(this.question_id).text;
      },
    },
    keywords() {
      return this.words.split(" ");
    },
  },
  methods: {
    clickMethod() {
      //window.location.href = 'https://www.google.com/';
    },
  },
};
</script>

<style scoped>
.output-container {
  overflow: auto;
  height: 128px;
}

input {
  margin: 0;
  padding: 0;
  width: 200px;
}
</style>