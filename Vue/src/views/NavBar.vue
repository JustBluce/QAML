<!--
Developers: Damian Rene
--> 

<template>
  <v-app-bar app>
    <v-toolbar-title>
      Adversarial Trivia Question Writing Interface
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn
      icon
      class="mr-2"
      @click="$vuetify.theme.dark = !$vuetify.theme.dark"
    >
      <v-icon>mdi-brightness-6</v-icon>
    </v-btn>

    <v-toolbar-items>
      <v-btn v-for="item in items" :key="item.title" :to="item.link">
        <v-icon class="mr-1">{{ item.icon }}</v-icon>
        {{ item.title }}
      </v-btn>
      <v-btn v-show="!user" @click="logOut">
        <v-icon class="mr-1">mdi-logout</v-icon>
        Logout
      </v-btn>
    </v-toolbar-items>
  </v-app-bar>
</template>

<script>
import firebase from "firebase";

export default {
  data() {
    return {
      user: null,
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
      let menuItems = [
        {
          title: "Login",
          icon: "mdi-login-variant",
          link: "/login",
        },
        {
          title: "About",
          icon: "mdi-information-outline",
          link: "/about",
        },
      ];
      return menuItems;
    },
  },
  methods: {
    logOut(e) {
      this.$router.push({ name: "Login" });
      e.stopPropagation();
      firebase.auth().signOut();
    },
  },
};
</script>