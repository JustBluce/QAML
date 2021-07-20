<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div class="Machine-Guess-container">
    <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Machine Guess</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in answer" :key="user.guess">
                    <td width="100">{{user.guess}}</td>
                    <td>{{user.score}}</td>
                </tr>
            </tbody>
        </table>
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";

export default {
  name: "MachineGuesses",
  props: {
    workspace_id: Number,
    widget_id: Number,
  },
  
  computed: {
    qa() {
      let qa_index = this.$store.getters.workspace(
        this.workspace_id
      ).qa_selected;
      return this.$store.getters.qa(this.workspace_id, qa_index);
    },
    
    answer() {
      return this.qa.answer;
    },
  },
};
</script>

<style scoped>
.Machine-Guess-container{
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 10px;
}

.container {
  cursor: default;
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
  background-color: #fffab8;
}
</style>