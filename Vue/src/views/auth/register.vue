<!--
Developers: Damian Rene and Jason Liu
--> 

<template>
  <v-container fill-height>
    <particles-bg :color="$vuetify.theme.currentTheme.primary" type="cobweb" />

    <v-card
      class="ma-auto pa-8 background justify-center"
      style="border-radius: 16px"
      elevation="16"
      min-width="600"
    >
      <v-card-title class="text-h3 justify-center">Register</v-card-title>

      <v-form ref="form" class="px-8">
        <v-text-field
          v-model="name"
          label="Name"
          placeholder="Name"
          :rules="nameRules"
        ></v-text-field>

        <v-text-field
          v-model="email"
          label="Email"
          placeholder="Email address"
          :rules="emailRules"
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Password"
          placeholder="Password"
          :rules="passwordRules"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          @click:append="showPassword = !showPassword"
        ></v-text-field>
      </v-form>

    

      <v-card-actions class="justify-center pb-4">
        <v-btn class="primary" @click="login">
          <v-icon left> mdi-account-plus </v-icon>
          Register
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import firebase from "firebase";
import { ParticlesBg } from "particles-bg-vue";

export default {
  name: "Register",
  components: {
    ParticlesBg,
  },
  data() {
    return {
      name: "",
      email: "",
      user: "",
      password: "",
      errors: [],
      showPassword: false,
      nameRules: [
        (v) => !!v || "Name is required",
        (v) => v.length >= 4 || "Min 4 characters",
      ],
      emailRules: [
        (v) => !!v || "E-mail is required",
        (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],
      passwordRules: [
        (v) => !!v || "Password is required",
        (v) => v.length >= 8 || "Min 8 characters",
      ],
    };
  },
  methods: {
    created() {
    firebase.auth().onAuthStateChanged((result) => {
      this.user = result;
    })
    },
    login() {
      firebase.auth().createUserWithEmailAndPassword(this.email, this.password).catch(function(error) {
      console.log(error.code);
      console.log(error.message);
      
    }).then((userCredential) => {
    // Signed in 
      this.user = userCredential.user
      //this.user = userCredential.user;
    // ...
  })
      this.createUser();
    },
    createUser() {
      
      const db = firebase.firestore();
      const docs = db.collection("users");
      let document_exists = false;

      db.collection("users")
        .where("email", "==", this.email)
        .get()
        .then((snapshot) => {
          snapshot.docs.forEach((doc) => {
            if (doc.exists) {
              document_exists = true;
            }
          });
          if (!document_exists) {
              db.collection("users").doc(this.user.uid).set({
                displayName: this.name,
                email: this.email,
                signInMethod: "Email and Password",
                CreatedTimestamp: firebase.firestore.Timestamp.now(),
                points: 0, 
              })
              .catch((err) => {
                alert("DOCUMENTS Oops. " + err.message);
              });
          }
        })
    }
  }
}
</script>