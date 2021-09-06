<!--
Developers: Damian Rene and Jason Liu
-->

<template>
  <v-card class="ma-4" v-if="user">
    <v-card-title> {{ user.displayName }}'s statistics </v-card-title>
    <v-divider></v-divider>
    <v-row class="pa-4 background" no-gutters>
      <v-card class="mr-4" elevation="4">
        <v-card-title>
          Question statistics
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-divider></v-divider>
        <v-data-table
          :headers="headers"
          :items="genreCount"
          :search="search"
          :sort-by="['Genre', 'Count']"
          :sort-desc="[true, false]"
          multi-sort
        ></v-data-table>
      </v-card>

      <v-card elevation="4">
        <v-card-title> Genre distribution </v-card-title>
        <v-divider></v-divider>
        <GChart type="PieChart" :options="options" :data="genreChartData" />
      </v-card>
    </v-row>
  </v-card>
</template>

<script>
import firebase from "firebase";
import { GChart } from "vue-google-charts";

export default {
  name: "WorkspaceStats",
  components: {
    GChart,
  },
  data() {
    return {
      user: null,
      genreCount: [],
      search: "",
      headers: [
        { text: "Genre", value: "Genre", width: "30%" },
        { text: "Count", value: "Count", width: "30%" },
      ],
      chartData: [
        ["Genre", "Number of Questions"],
        ["2014", 1000],
        ["2015", 1170],
        ["2016", 660],
        ["2017", 1030],
      ],
      options: {
        width: 500,
        backgroundColor: "none",
      },
    };
  },
  computed: {
    genreChartData() {
      return this.$store.state.genreChartData;
    },
  },
  mounted() {
    this.user = firebase.auth().currentUser;
    this.axios({
      url: "http://127.0.0.1:5000/genres/getGenre",
      method: "GET",
      params: {
        uid: this.user.uid,
      },
    }).then((response) => {
      this.genreCount = response.data;
      console.log(response);
    });
  },
};
</script>
