<!--
Developers: Damian Rene and Jason Liu
-->

<template>


      <v-card class="ma-4 pa-2 " style="display: block; border-radius: 5%" max-width="400" elevation="4">

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
    const user = firebase.auth().currentUser;
    this.axios({
      url: "http://127.0.0.1:5000/genre_classifier/genre_data",
      method: "GET",
      params: {
        uid: user.uid,
      },
    }).then((response) => {
      this.genreCount = response.data;
      console.log(response);
    });
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user.email) {
        this.user = user;
      }
    });
  },
};
</script>


<style scoped>
.workspace-container {
  overflow-y: auto;
  
  
}


.leaderboard-title{
  
  background-color: #8ecae6;
}

</style>