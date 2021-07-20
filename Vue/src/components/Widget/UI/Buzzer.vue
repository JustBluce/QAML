<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div class="Buzzer-container">
    <!-- <textarea
      readonly
      class="container"
      rows="5"
      placeholder="Buzzer"
      v-model="binary_search_based_buzzer"
    ></textarea> -->
    <Highlighter
      :style="{ color: 'black' }"
      highlightClassName="highlight"
      :searchWords="keywords"
      :autoEscape="true"
      :textToHighlight="binary_search_based_buzzer"
    />
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>Sentence</th>
          <th>Importance</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in importance" :key="user.sentence">
          <td>{{ user.sentence }}</td>
          <td>{{ user.importance }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";
export default {
  name: "Buzzer",
  props: {
    workspace_id: Number,
    widget_id: Number,
  },
  components: {
    Highlighter,
  },
  data() {
    return {
      words: "🔔BUZZ",
    };
  },
  computed: {
    qa() {
      let qa_index = this.$store.getters.workspace(
        this.workspace_id
      ).qa_selected;
      return this.$store.getters.qa(this.workspace_id, qa_index);
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
.Buzzer-container {
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