<!--
Developers: Cai Zefan, Jason Liu, and Damian Rene
-->

<template>
  <v-card class="ma-4">
    <v-card-title>
      Leaderboard
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
      :items="leaderboard"
      :search="search"
      :sort-by="['Score', 'Name']"
      :sort-desc="[true, false]"
      multi-sort
    ></v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "Leaderboard",
  data() {
    return {
      search: "",
      headers: [
        { text: "Name", value: "Name", width: "30%" },
        { text: "Score", value: "Score", width: "30%" },
      ],
      leaderboard: [],
    };
  },
  mounted() {
    this.axios({
      url: "http://127.0.0.1:5000/users/leaderboard",
      method: "GET",
    }).then((response) => {
      this.leaderboard = response.data;
      console.log(response);
    });
  },
};
</script>