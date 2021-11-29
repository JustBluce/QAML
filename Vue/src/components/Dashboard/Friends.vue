<!--
Developers: Damian Rene
-->

<template>
  <v-card class="ma-4">
    <v-card-title>
      Friends
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
      :sort-by="['Name']"
      :sort-desc="[true]"
      multi-sort
    ></v-data-table>
  </v-card>
</template>

<script>
import firebase from "firebase";


export default {
  name: "Friends",
  components: {
    
  },
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      user: "",
      emailRules: [
        (v) => !!v || "E-mail is required",
        //(v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],
      passwordRules: [
        (v) => !!v || "Password is required",
        // (v) => v.length >= 8 || "Min 8 characters",
      ],
      search: "",
      headers: [
        { text: "Name", value: "Name", width: "100%" },
      ],
      leaderboard: [ 'jim','joe'],
    };
  },
  methods: {
    getFriends() {
      const db = firebase.firestore();
      const docs = db.collection("users");
      let document_exists = false;

      db.collection('users').doc('kvyXZ8ZnY9WnuWzNhUipk28h68G2').collection('friends').doc('friendslist')
      .get()
      .then((doc) => {
        console.log(doc.data ())
        //this.leaderboard.push(doc.data())
          
      })
        
      
     
      
    },
   
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        this.user = user;
        this.getFriends()
        
        console.log(this.user)
      }
    });
  },
};
</script>