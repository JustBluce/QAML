<!--
Developers: Cai Zefan, Jason Liu, and Damian Rene
-->

<template>
  <v-container>
    <v-card-title class="primary white--text rounded-lg">
      Leaderboard
      <v-spacer></v-spacer>
      <v-text-field
        dark
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>

    <v-flex style="overflow: auto; height: 70vh; border-radius: 10px">
      <v-data-table
        dense
        :headers="headers"
        :items="leaderboard"
        :items-per-page="itemsPerPage"
        :footer-props="{
          'items-per-page-options': [10, 20, 30, -1],
        }"
        :search="search"
        :sort-by="['Score']"
        :page.sync="page"
        :sort-desc="[true]"
        no-data-text="We are having trouble accessing the leaderboard right now."
        hide-default-footer
      >
      </v-data-table>
      <v-pagination v-model="page" :length="pageCount" circle> </v-pagination>
    </v-flex>
  </v-container>
</template>
<script>
import firebase from "firebase";

export default {
  name: "Online_Status",
  data() {
    return {
      search: "",
      name: "",
      points: "",
      page: 1,
      itemsPerPage: 10,
      headers: [
        { text: "Name", value: "Name", width: "30%" },
        { text: "Score", value: "Score", width: "30%" },
      ],
      leaderboard: [],
    };
  },
  computed: {
    totalRecords() {
      return this.leaderboard.length;
    },
    pageCount() {
      return Math.round(this.totalRecords / this.itemsPerPage);
    },
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

  created() {
    this.user = firebase.auth().currentUser;

    const db = firebase.firestore();
    const docs = db.collection("users");
    //Send name and points of all users to dashboard on first load

    db.collection("users").onSnapshot((res) => {
      const changes = res.docChanges();
      changes.forEach((change) => {
        if (change.type === "added") {
          this.leaderboard.push({
            Name: change.doc.data().displayName,
            Score: change.doc.data().points,
            Id: change.doc.id,
          });
        }
      });
    });
    //updates points on change in firestore
    //added
    //removed
    //modified
    db.collection("users").onSnapshot((res) => {
      const changes = res.docChanges();
      changes.forEach((change) => {
        if (change.type === "modified") {
          this.leaderboard.length = 0;
          docs.get().then((snapshot) => {
            snapshot.forEach((doc) => {
              this.leaderboard.push({
                Name: doc.data().displayName,
                Score: doc.data().points,
                Id: doc.id,
              });
            });
          });
        }
      });
    });
  },
};
</script>

<style >
.v-data-table > .v-data-table__wrapper > table > tbody > tr > td,
.v-data-table > .v-data-table__wrapper > table > tfoot > tr > td,
.v-data-table > .v-data-table__wrapper > table > thead > tr > td {
  font-size: 12px;
  padding: 3%;
}
</style>