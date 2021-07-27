<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>

  <div class="country_representation-container">
    <div>
    <h4>Please consider adding the following under-represented countries for 10 extra points</h4>
    </div>
    <table class="table table-striped table-bordered">
            <thead>
                <!-- <tr>
                    <th>Please consider adding the following under-represented countries for 10 extra points</th> 
                </tr> -->
            </thead>
            <tbody>
                <tr v-for="user in country_representation" :key="user.Country">
                    <td style="text-align: center">
                      {{user.Country}}
                      

                    </td>
                    <!-- <td>{{user.Score}}</td> -->
                </tr>
            </tbody>
        </table>
    
  </div>
</template>

<script >
export default {
  name: "CountryRepresentation",
  props: {
    workspace_id: Number,
    widget_id: Number,
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    country_representation() {
      console.log(this.qa.country_representation)
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