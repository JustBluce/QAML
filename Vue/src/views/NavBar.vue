<!-- Nav Bar Login: Damian Rene--> 
<template>
    <!-- display the navigation bar -->
    
    <v-toolbar elevation="4">
    <v-toolbar-title style="color:black;">Adversarial Trivia Question Writing Interface</v-toolbar-title>

      <v-spacer></v-spacer>
<!-- navigation bar links You can add more in the computed items -->

      <v-toolbar-items class='hidden-xs-only'>

        <v-btn  class="mx-2"  v-for="item in items" :key="item.title" :to="item.link">
          <v-icon class="nav-button-icon" right>{{item.icon}}</v-icon>{{item.title}}
        </v-btn>
        <v-spacer></v-spacer>
      </v-toolbar-items>


      <!-- sign out button (You can chnage to only show when logged in, but then the Navbar looks empty)-->
      <v-toolbar-items class='hidden-xs-only'>
        <v-btn v-show="!user" @click="signOut"
        class="mx-2"
          flat
          >
          <v-icon class="nav-button-icon" right>mdi-logout</v-icon>Logout
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
   
</template>
<script>
import firebase from "firebase";

export default {
    data() {
    return {
        user: null
    };
},
/*
updated() {
    firebase.auth().onAuthStateChanged(user => {
        this.user = user;
    });
    
},
*/
  computed: {
    items() {
      let menuItems =  [
          {
          title: 'Login',
          icon: 'mdi-login-variant',
          link: '/login'
        },
        {
          title: 'About',
          icon: 'mdi-login-variant',
          link: '/about'
        }
      ]
    return menuItems
    }
  },
  methods: {
    signOut(e) {
      alert("Signed Out!");
      this.$router.push({name: "Login"});
        e.stopPropagation();
        firebase.auth().signOut();
        
    }
}
}
</script>

<style scoped>
.toolbar{
  background: #50759e;
 
}
.nav-button-icon{
  margin-right: 5px;

}
</style>