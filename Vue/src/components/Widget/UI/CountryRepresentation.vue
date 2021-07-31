<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div>
    <h4 class="mb-2">
      Please consider adding the following under-represented countries for 10
      extra points
    </h4>
    <v-data-table
      hide-default-header
      hide-default-footer
      :headers="headers"
      :items="countries"
      class="elevation-2"
    ></v-data-table>
  </div>
</template>

<script >
export default {
  name: "CountryRepresentation",
  props: {
    workspace_id: Number,
  },
  data() {
    return {
      headers: [{ text: "Country", value: "Country" }],
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    countries() {
      console.log(this.qa.country_representation);
      return this.qa.country_representation;
    },
    people_ethnicity() {
      return this.qa.people_ethnicity;
    },
  },
};
</script>

<style scoped>
.representation-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.container {
  cursor: default;
}
</style>