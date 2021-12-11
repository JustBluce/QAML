<!--
Developers: Atith Gandhi, Raj Shah and Jason Liu
-->

<template>
  <div>
    <h4 class="mb-2">
      Please consider adding the following under-represented countries for 10
      extra points
    </h4>
    <v-data-table
      :headers="headers"
      :items="country_representation"
      :expanded.sync="expanded"
      item-key="id"
      show-expand
      hide-default-header
      hide-default-footer
      dense
      class="elevation-2 background"
    >
      <template #item.answer="{ item }">
        <a
          target="_blank"
          :href="links[item.answer]"
          :style="{
            color: links[item.answer]
              ? $vuetify.theme.currentTheme.primary
              : $vuetify.theme.currentTheme.red,
          }"
        >
          {{ item.answer }}
        </a>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          {{ item.text }}
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import wiki from "wikijs";

export default {
  name: "CountryRepresentation",
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
      links: {},
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    // country_representation() {
    //   return this.qa.country_representation;
    // },
    country_representation() {
      if (this.qa.country_representation) {
        return this.qa.country_representation.map((question, index) => {
          wiki({ apiUrl: "https://en.wikipedia.org/w/api.php" })
            .page(question.answer)
            .then((page) => {
              this.$set(this.links, question.answer, page.url());
            })
            .catch((e) => {});
          return Object.assign(question, { id: index });
        });
      }
      return [];
    },
  },
};
</script>