<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div class="Buzzer-container">
    <textarea
      readonly
      class="container"
      rows="5"
      placeholder="Buzzer"
      v-model="binary_search_based_buzzer"
    ></textarea>
    <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Sentence</th>
                    <th>Importance</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in importance" :key="user.id">
                    <td>{{user.sentence}}</td>
                    <td>{{user.importance}}</td>
                </tr>
            </tbody>
        </table>
  </div>
</template>

<script>
export default {
  name: "Buzzer",
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
    binary_search_based_buzzer() {
      return this.qa.binary_search_based_buzzer;
    },
    importance() {
      return this.qa.importance;
    }
  },
};
</script>

<style scoped>
.Buzzer-container{
  display: flex;
  flex-direction: column;
  width: 100%;
}

.container {
  cursor: default;
}
</style>