<template>
  <v-menu bottom rounded offset-y min-width="125">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-avatar size="36px" v-if="user && user.photoURL">
          <img v-if="user.photoURL" :src="user.photoURL" />
        </v-avatar>
        <v-icon size="36px" v-else>mdi-account-circle</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-list-item-content class="justify-center">
        <div class="mx-auto text-center">
          <h3 class="pa-2">{{ user ? user.displayName : "Guest" }}</h3>
          <v-divider class="my-1"></v-divider>
          <v-btn depressed rounded text href="/about"> About </v-btn>
          <v-divider class="my-1"></v-divider>
          <v-btn
            depressed
            rounded
            text
            target="_blank"
            href="https://github.com/JustBluce/TryoutProject"
          >
            GitHub
          </v-btn>
          <v-divider class="my-1"></v-divider>
          <v-btn depressed rounded text @click.native="logout"> Logout </v-btn>
        </div>
      </v-list-item-content>
    </v-card>
  </v-menu>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Profile",
  data() {
    return {
      user: null,
    };
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user.email) {
        this.user = user;
      }
    });
  },
  methods: {
    logout(e) {
      this.$router.push({ name: "Login" });
      e.stopPropagation();
      firebase.auth().signOut();
      this.$store.dispatch("fetchUser", null);
    },
  },
};
</script>