<!--
Developers: Jason Liu, Damian Rene, and Cai Zefan
-->

<template>
  <div>
    <Taskbar title="Dashboard" />

    <v-card class="ma-4 pa-2" max-width="400">
      <v-card-title>
        <v-avatar size="56" v-if="user">
          <img alt="user" :src="user.photoURL" />
        </v-avatar>
        <v-icon size="56" v-else>mdi-account-circle</v-icon>
        <p class="text-h4 ml-3 mb-0">Profile</p>
      </v-card-title>
      <v-card-text>
        <div class="text--primary text-body-1" v-if="user">
          Name: <strong>{{ user.displayName }}</strong
          ><br />
          Email: <strong>{{ user.email }}</strong
          ><br />
          Provider: <strong>{{ user.providerData[0].providerId }}</strong>
        </div>
        <div v-else>Logged in as guest</div>
      </v-card-text>
    </v-card>

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
      <v-data-table
        :headers="headers"
        :items="leaderboard"
        :search="search"
        :sort-by="['Score', 'Name']"
        :sort-desc="[true, false]"
        multi-sort
      ></v-data-table>
    </v-card>
  </div>
</template>

<script>
import firebase from "firebase";
import Taskbar from "@/components/Taskbar";

export default {
  name: "Data",
  components: {
    Taskbar,
  },
  data() {
    return {
      user: null,
      search: "",
      headers: [
        { text: "Name", value: "Name", width: "30%" },
        { text: "Score", value: "Score", width: "30%" },
        { text: "LastLogin", value: "LastLogin", width: "40%" },
      ],
      leaderboard: [],
    };
  },
  methods: {
    updateUserProfile() {
      // [START auth_update_user_profile]
      const user = firebase.auth().currentUser;

      user
        .updateProfile({
          photoURL: user.photoURL,
        })
        .then(() => {
          alert("yay");
          // Update successful
          // ...
        })
        .catch((error) => {
          alert(error);
          // An error occurred
          // ...
        });
    },
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        this.user = user;
      }
    });
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
