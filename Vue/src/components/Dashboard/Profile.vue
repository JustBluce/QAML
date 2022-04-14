<!--
Developers: Damian Rene and Jason Liu
-->

<template>
  <v-card class="leaderboard-title ma-4 pa-2 " elevation=4 style="display: block; border-radius: 5%; " max-width="350">
    <v-card-title >
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
          <!--
        <p class="font-weight-thin" style="margin-right: auto; margin-left:auto;">Questions</p>
      -->
      
        <p class="font-weight-thin" style="margin-right: auto; margin-left:auto;">Points</p>
         <!--
        <p class="font-weight-thin" style="margin-right: auto; margin-left:auto;">Followers</p>
        -->
       </v-row>
       <v-row >
         <!--
        <p class="font-weight-bold" style="margin-right: auto; margin-left:auto;">25</p>
      -->
        <p class="font-weight-bold" style="margin-right: auto; margin-left:auto;" >{{points}}</p>
         <!--
        <p class="font-weight-bold" style="margin-right: auto; margin-left:auto;">20</p>
        -->
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
      points: 0, 
      db: null, 
      status: "",
      docs: null, 
    };
  },
  methods: {
    mounted(){
        this.getConnectionStatus();
    },
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
    this.user = firebase.auth().currentUser;
    const UID = this.user.uid
    const db = firebase.firestore();
    this.db = db
    const docs = db.collection("users");

    const userStatusDatabaseRef = firebase.database().ref('/status/' + UID);
    const isOfflineForDatabase = {
      status_state: 'offline',
      //status_last_changed: firebase.database.ServerValue.TIMESTAMP,
    };

    const isOnlineForDatabase = {
        status_state: 'online',
        //status_last_changed: firebase.database.ServerValue.TIMESTAMP,
    };

    firebase.database().ref('.info/connected').on('value', function(snapshot) {
    // If we're not currently connected, don't do anything.
    if (snapshot.val() == false) {
        return;
    };
    userStatusDatabaseRef.onDisconnect().set(isOfflineForDatabase).then(function() {
        userStatusDatabaseRef.set(isOnlineForDatabase);
    });
    })
   

    //Get status
    //Sets points on dashboard initially
    docs.where('email', '==', this.user.email).get().then( snapshot => {
        snapshot.forEach(doc => {
          this.points = doc.data().points;
          //console.log(doc.id, '=>', doc.data().points);
      });

    })
      
    //updates points on change in firestore
    docs.onSnapshot(res => {
      const changes = res.docChanges()

      changes.forEach(change => {
        if (change.type === 'modified'){
          //console.log(change.doc.data().points)
          this.points = change.doc.data().points
        }
      })
    })
    
      // Get a database reference to our posts
    
    const ref = firebase.database().ref('/status/' + UID);

    // Attach an asynchronous callback to read the data at our posts reference

    firebase.database().ref('status').child(UID).child('status_state').get()
      .then ((snapshot) => {
          this.status = snapshot.val()
      });


  }
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
.leaderboard-title{
  background-color: #8ecae6;
  color: #8ecae6;
}



</style> 