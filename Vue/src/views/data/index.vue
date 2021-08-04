<template>
  <v-main>
    <Taskbar title="Data" />
    <v-card class="ma-2">
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
      <v-data-table
        :headers="headers"
        :items="leaderboard"
        :search="search"
        :sort-by="['Score', 'Name']"
        :sort-desc="[true, false]"
        multi-sort
      ></v-data-table>
    </v-card>
  </v-main>
</template>

<script>
import Taskbar from "@/components/Taskbar";

export default {
  name: "Data",
  components: {
    Taskbar,
  },
  data() {
    return {
      search: "",
      headers: [
        { text: "Name", value: "Name", width: "30%" },
        { text: "Score", value: "Score", width: "30%" },
        { text: "LastLogin", value: "LastLogin", width: "40%" },
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