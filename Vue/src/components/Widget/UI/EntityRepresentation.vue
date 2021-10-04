<!--
Developers: Atith Gandhi, Raj Shah and Jason Liu
-->

<template>
  <div>
    <h4 class="mb-2">
      Please consider adding the following under-represented entities for 10
      extra points
    </h4>
    <v-data-table
      :headers="headers"
      :items="entity_representation"
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
            item.text
          }}</span>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "EntityRepresentation",
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
    // entity_representation() {
    //   return this.qa.entity_representation;
    // },
    entity_representation() {
      if (this.qa.entity_representation) {
        return this.qa.entity_representation.map((question, index) =>
          Object.assign(question, { id: index })
        );
      }
      return [];
    },
  },
};
</script>