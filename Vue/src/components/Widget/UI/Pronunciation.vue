<!--
Developers: Damien Rene and Jason Liu
-->

<template>
  <div readonly class="container output" @click="clickMethod">
    <div class="placeholder" v-show="!text">Please enter your question</div>
    <Highlighter
      :style="{ color: 'black' }"
      highlightClassName="highlight"
      :searchWords="keywords"
      :autoEscape="true"
      :textToHighlight="text"
    />
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";
export default {
  name: "Pronunciation",
  props: {
    workspace_id: Number,
    widget_id: Number,
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
    text() {
      let qa_index = this.$store.getters.workspace(this.workspace_id).qa_selected;
      return this.$store.getters.qa(this.workspace_id, qa_index).text;
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
select {
  cursor: pointer;
  opacity: 1;
  transition: opacity 0.3s;
}

select:hover {
  opacity: 0.7;
}

.output {
  cursor: default;
  height: 172px;
}

.placeholder {
  color: #757575;
}

.highlight {
  background-color: #c8ebfb;
}
</style>