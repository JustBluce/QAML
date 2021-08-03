<template>
    <!-- display the navigation bar -->
    
    <v-toolbar elevation="4">
    <v-toolbar-title style="color:black;">Adversarial Trivia Question Writing Interface</v-toolbar-title>

      <v-spacer></v-spacer>
<!-- navigation bar links You can add more in the computed items -->

      <v-toolbar-items class='hidden-xs-only'>

        <v-btn  class="mx-2"  v-for="item in items" :key="item.title" :to="item.link">
          <v-icon right>{{item.icon}}</v-icon>{{item.title}}
        </v-btn>
        <v-spacer></v-spacer>
      </v-toolbar-items>


      <!-- sign out button -->
      <v-toolbar-items class='hidden-xs-only'>
        <v-btn v-show="!user" @click="signOut"
        class="mx-2"
          flat
          >
          <v-icon right>mdi-logout</v-icon>Logout
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
   
</template>
<script>


export default {
    data() {
    return {
        user: null
    };
},
created() {
    firebase.auth().onAuthStateChanged(user => {
        this.user = user;
    });
},
  computed: {
    items() {
      let menuItems =  [
          {
          title: 'Login',
          icon: 'mdi-login-variant',
          link: '/login'
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
</style>