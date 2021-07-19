<!--
Developers: Damien Rene and Jason Liu
-->

<template>
  <div class="Pronunciation-container">
    <!-- <div class="placeholder" v-show="!text">Please enter your question</div>
    <Highlighter
      :style="{ color: 'black' }"
      highlightClassName="highlight"
      :searchWords="keywords"
      :autoEscape="true"
      :textToHighlight="text"
    /> -->
    <div>
      <h4> Please add the pronunciation guide for the following words </h4>
    </div> 
    <textarea
      readonly
      class="container"
      rows="1"
      placeholder="Pronunciation "
      v-model="pronunciation"
    ></textarea>
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
      let qa_index = this.$store.getters.workspace(
        this.workspace_id
      ).qa_selected;
      return this.$store.getters.qa(this.workspace_id, qa_index);
    },
    text() {
      let qa_index = this.$store.getters.workspace(this.workspace_id).qa_selected;
      return this.$store.getters.qa(this.workspace_id, qa_index).text;
    },
    pronunciation() {
      return this.qa.pronunciation;
    },
    keywords() {
      return this.words.split(" ");
    },
  },
  methods: {
    
  },
};
</script>

<style scoped>
.Pronunciation-container{
  display: flex;
  flex-direction: column;
  height: 300px;
  width: 100%;
}
.container{
  display: flex;
  flex-direction: column;
 height: 300px;
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
