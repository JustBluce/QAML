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
      :sort-by="['Score']"
      :sort-desc="[true]"
      
      multi-sort
    ></v-data-table>
  </v-card>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Leaderboard",
  data() {
    return {
      search: "",
      name: "", 
      points: "", 
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
    created() {
      this.user = firebase.auth().currentUser;

      const db = firebase.firestore();
      const docs = db.collection("users");
  //Send name and points of all users to dashboard on first load
    
        db.collection("users").onSnapshot(res => {
          const changes = res.docChanges()
          changes.forEach(change => {
            if (change.type === 'added'){
                this.leaderboard.push({
                  Name: change.doc.data().displayName, 
                  Score: change.doc.data().points,
                  Id: change.doc.id
              })

            }
          })
        })
      //updates points on change in firestore
      //added
      //removed
      //modified
        db.collection("users").onSnapshot(res => {
          const changes = res.docChanges()
          changes.forEach(change => {
          if (change.type === 'modified'){
            this.leaderboard.length = 0
            docs.get().then( snapshot => {
              snapshot.forEach(doc => {
                this.leaderboard.push({
                    Name: doc.data().displayName, 
                    Score: doc.data().points,
                    Id: doc.id
                })
              
            })
          
          })
          }
          }) 
          })

    },
    


};
</script>