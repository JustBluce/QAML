<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div class="representation-container">
    <textarea
      readonly
      class="container"
      rows="5"
      placeholder="People ethnicity"
      v-model="people_ethnicity"
    ></textarea>
    <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Please consider adding the following under-represented countries for 10 extra points</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in country_representation" :key="user.id">
                    <td>{{user.Country}}</td>
                    
                </tr>
            </tbody>
        </table>
    
  </div>
</template>

<script>
export default {
  name: "Representation",
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
    country_representation() {
      return this.qa.country_representation;
    },
    people_ethnicity() {
      return this.qa.people_ethnicity;
    }
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