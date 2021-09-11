<!--
Developers: Jason Liu and Damian Rene
-->

<template>
  <div>
    <v-btn id="profile" icon>
      <v-avatar size="44px" v-if="email && user.photoURL">
        <img v-if="user.photoURL" :src="user.photoURL" />
      </v-avatar>
      <v-icon size="44px" v-else>mdi-account-circle</v-icon>
      <v-tooltip bottom activator="#profile">
        <span>User profile</span>
      </v-tooltip>
      <v-menu
        bottom
        rounded
        transition="fade-transition"
        offset-y
        min-width="180"
        activator="#profile"
      >
        <v-card>
          <v-list-item-content class="justify-center">
            <div class="mx-auto text-center">
              <h3 v-if="user" class="pa-2">
                {{ email ? user.displayName : "Guest" }}
              </h3>
              <h3 v-else class="pa-2">Not signed in</h3>
              <v-divider class="my-1"></v-divider>
              <v-btn
                v-if="navbar"
                :disabled="user == null"
                depressed
                rounded
                text
                @click="$router.push('dashboard').catch(() => {})"
              >
                Dashboard
              </v-btn>
              <v-btn
                v-else
                depressed
                rounded
                text
                @click="$router.push('about').catch(() => {})"
              >
                About
              </v-btn>
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
              <v-btn v-if="user" depressed rounded text @click="logout">
                Logout
              </v-btn>
              <v-btn
                v-else
                depressed
                rounded
                text
                @click="$router.push('login').catch(() => {})"
                >Login
              </v-btn>
              <div v-if="email">
                <v-divider class="my-1"></v-divider>
                <v-btn depressed rounded text color="red" @click="popup = true">
                  Delete Account
                </v-btn>
              </div>
            </div>
          </v-list-item-content>
        </v-card>
      </v-menu>
    </v-btn>

    <v-dialog v-model="popup" persistent max-width="500">
      <v-card>
        <v-card-title class="text-h5"> Account deletion </v-card-title>
        <v-card-text
          >Are you sure you want to delete your account? This will erase all of
          your data and progress PERMANENTLY.</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="popup = false">
            Cancel
          </v-btn>
          <v-btn color="red" text @click="deleteAccount">
            Delete Account
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Profile",
  props: {
    navbar: Boolean,
  },
  data() {
    return {
      user: null,
      email: false,
      document: null,
      popup: false,
    };
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        this.user = user;
        if (user.email) {
          this.email = true;
        }
      }
    });
  },
  methods: {
    logout() {
      this.$router.push("login").catch(() => {});
      firebase.auth().signOut();
      //this.$store.dispatch("fetchUser", null);
    },
    deleteAccount() {
      const db = firebase.firestore();
      this.user = firebase.auth().currentUser;

      db.collection("users")
        .where("email", "==", this.user.email)
        .get()
        .then((snapshot) => {
          snapshot.docs.forEach((doc) => {
            this.document = doc;
            const data = doc.data();

            console.log(data);

            console.log("Deleting documents and erasing all data. Goodbye.");
          });
        });
      const docs = this.document;
      db.collection("users")
        .docs.delete()
        .then(() => {
          console.log("document deleted");
        });
    },
  },
};
</script>