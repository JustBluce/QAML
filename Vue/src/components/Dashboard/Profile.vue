<!--
Developers: Damian Rene and Jason Liu
-->

<template>
  <v-card class="ma-4 pa-2 " style="display: block; border-radius: 5%; " max-width="400">
    <v-card-title>
      <v-avatar class="avatar" size="66" v-if="user && user.photoURL">
        <img alt="user" :src="user.photoURL" />
      </v-avatar>
      <v-icon size="56" v-else>mdi-account-circle</v-icon>
      
    </v-card-title>
    <v-card-text>
      <div class="text--primary text-body-1" v-if="user">
        <strong class="name">{{ user.displayName }}</strong
        ><br />
        <div style="margin-bottom: 5%;"></div>
        <v-row>
        <p class="font-weight-thin" style="margin-right: auto; margin-left:auto;">Questions</p>
      
        <p class="font-weight-thin" style="margin-right: auto; margin-left:auto;">Answers</p>
         
        <p class="font-weight-thin" style="margin-right: auto; margin-left:auto;">Followers</p>
       </v-row>
       <v-row >
        <p class="font-weight-bold" style="margin-right: auto; margin-left:auto;">25</p>
      
        <p class="font-weight-bold" style="margin-right: auto; margin-left:auto;">25</p>
         
        <p class="font-weight-bold" style="margin-right: auto; margin-left:auto;">20</p>
       </v-row>
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
      const user = firebase.auth().currentUser;
      if (user?.isAnonymous) {
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


<style> 
.avatar{
  display: block;
  margin-left: auto;
  margin-right: auto;

}
.name{
  display: block;
  text-align: center;
  font-size: 140%;
  

}


</style> 