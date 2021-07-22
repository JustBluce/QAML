<!--
Developers: Damien Rene and Jason Liu
-->

<template>
  <div class="Pronunciation-container">
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
    <v-textarea
      readonly    
      color="background"
      rows="1"
      placeholder="Pronunciation highlighting"
      v-model="pronunciation"
    ></v-textarea>
    <!-- <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Original_Word</th>
                    <th>Transcribed_Word</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in pronunciation" :key="user.Original_Word">
                    <td>{{user.Original_Word }}</td>
                    <td>{{user.Transcribed_Word }}</td>
                    <td>{{user.Score}}</td>
                </tr>
            </tbody>
        </table> -->
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

<style scoped>
.Pronunciation-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}
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
