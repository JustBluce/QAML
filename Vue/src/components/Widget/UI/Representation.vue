<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div class="representation-container">
    <textarea
      readonly
      class="container"
      rows="1"
      placeholder="Genre"
      v-model="qa.genre"
    ></textarea>
    <GChart type="PieChart" :options="options" :data="subgenre" />
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th colspan="2">
            Please consider adding the following under-represented countries for
            10 extra points
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in country_representation" :key="user.Country">
          <td>{{ index + 1 }}. {{ user.Country }}</td>
          <!-- <td>{{ user.Score }}</td> -->
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script >
import { GChart } from "vue-google-charts";
export default {
  name: "Representation",
  props: {
    workspace_id: Number,
  },
  components: {
    GChart,
  },
  data() {
    return {
      data: [
        ["Daily Routine", "Hours per Day"],
        ["Work", 14],
        ["Eat", 1],
        ["Reading", 2],
        ["Exercise", 2],
        ["Sleep", 5],
      ],
      options: {
        width: 300,
        height: 300,
      },
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    country_representation() {
      console.log(this.qa.country_representation);
      return this.qa.country_representation;
    },
    people_ethnicity() {
      return this.qa.people_ethnicity;
    },
    genre() {
      return this.qa.genre;
    },
    subgenre() {
      if (this.qa.subgenre === "") {
        return [
          ["Subgenre", "Count"],
          ["None", 1],
        ];
      } else {
        let header = [["Subgenre", "Count"]];
        console.log(header.concat(this.qa.subgenre));
        return header.concat(this.qa.subgenre);
      }
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