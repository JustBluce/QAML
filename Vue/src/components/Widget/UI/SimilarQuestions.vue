<!--
Developers: Atith Gandhi, Raj Shah and Jason Liu
-->

<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="similar_questions"
      :expanded.sync="expanded"
      item-key="id"
      show-expand
      hide-default-header
      hide-default-footer
      dense
      class="elevation-2 background"
    >
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <span :style="{ color: $vuetify.theme.currentTheme.primary }">{{
           "Question: " + item.text 
          }}</span>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "SimilarQuestions",
  props: {
    workspace_id: Number,
  },
  data() {
    return {
      expanded: [],
      headers: [
        { text: "Answer", value: "answer" },
        { text: "", value: "data-table-expand", align: "right" },
      ],
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    country_representation() {
      return this.qa.country_representation;
    },
    similar_questions() {
      if (this.qa.top5_similar_questions[1]) {
        return this.qa.top5_similar_questions[1].map((question, index) =>
          Object.assign(question, { id: index })
        );
      }
      return [];
    },
  },
};
</script>