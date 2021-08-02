<template>
  <v-main>
    <Taskbar title="Dashboard" />
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
        :sort-by="['points', 'name']"
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
        { text: "Name", value: "name", width: "70%" },
        { text: "Points", value: "points", width: "30%" },
      ],
      leaderboard: [
        { name: "Alice", points: "0" },
        { name: "Bob", points: "100" },
        { name: "Carol", points: "200" },
        { name: "David", points: "300" },
        { name: "Eve", points: "400" },
        { name: "Frank", points: "500" },
        { name: "Grace", points: "600" },
        { name: "Heidi", points: "700" },
        { name: "Ivan", points: "800" },
        { name: "Judy", points: "900" },
        { name: "Mallory", points: "1000" },
        { name: "Victor", points: "1000" },
        { name: "Wendy", points: "1000" },
      ],
    };
  },
};
</script>