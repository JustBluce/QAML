<!--
Developers: Damian Rene and Jason Liu
-->

<template>
  <v-card class="ma-4 pa-2" max-width="400">
    <v-card-title>
      <v-avatar size="56" v-if="user && user.photoURL">
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
        Verified:
        <v-icon v-if="user.emailVerified" color="green">
          mdi-check-circle </v-icon
        ><v-icon v-else color="red"> mdi-close-circle </v-icon><br />
        Provider: <strong>{{ user.providerData[0].providerId }}</strong>
      </div>
      <div v-else>Logged in as guest</div>
    </v-card-text>
  </v-card>
</template>

<script>
import firebase from "firebase";

export default {
  name: "DashboardProfile",
  data() {
    return {
      user: null,
    };
  },
  methods: {
    test() {
      this.user = firebase.auth().currentUser;
      if (this.user?.isAnonymous) {
        console.log("ANONYMOUS!!!");
      }
    },
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
      if (user.email) {
        this.user = user;
      }
    });
  },
};
</script>