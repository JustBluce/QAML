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
      <v-card-title class="text-h3 justify-center">Login</v-card-title>

      <v-form ref="form" class="px-8">
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
          @keydown.enter="emailLogin"
        ></v-text-field>
      </v-form>

      <router-link
        class="ma-auto pa-8 background justify-center"
        :to="{ name: 'Password-Reset' }"
      >
        Forgot Password?
      </router-link>

      <v-card-actions class="justify-center pb-4">
        <v-btn class="primary" @click="emailLogin">
          <v-img
            class="mr-2"
            width="20px"
            alt="Email sign-in"
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/mail.svg "
          ></v-img>
          Email login
        </v-btn>
      </v-card-actions>
      <v-divider></v-divider>
      <v-card-actions class="justify-center pa-4">
        <v-btn class="red" @click="socialLogin">
          <v-img
            class="mr-2"
            width="20px"
            alt="Google sign-in"
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
          ></v-img>
          Google login
        </v-btn>
        <v-btn @click="guestLogin">
          <v-icon left size="20">mdi-account-circle</v-icon>
          Guest login
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import firebase from "firebase";
import { ParticlesBg } from "particles-bg-vue";

export default {
  name: "Login",
  components: {
    ParticlesBg,
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
    };
  },
  methods: {
    emailLogin() {
      if (this.$refs.form.validate()) {
        firebase
          .auth()
          .signInWithEmailAndPassword(this.email, this.password)
          .then(() => {
            this.$router.push("/dashboard");
          })
          .catch((error) => {
            alert(error.message);
          });
      }
    },
     socialLogin() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase
        .auth()
        .signInWithPopup(provider)
        .then( () => {
          //var user_name = result.user;
          // this.qa.uid = user.uid
          //console.log(this.qa.uid);
          this.$router.push("/dashboard");
          this.user = firebase.auth().currentUser;
          this.documents();
          
        })
        .catch((err) => {
          alert("Login Error. " + err.message);
        });
    },
    documents() {
      
      
      const db = firebase.firestore();
      const docs = db.collection("users");
      let document_exists = false;
      let lastUser = 0;
      
      db.collection("users")
        .where("email", "==", this.user.email)
        .get()
        .then((snapshot) => {
          snapshot.docs.forEach((doc) => {
            if (doc.exists) {
              console.log("Firebase Document already exsists. Easy for me. thanks");
              //console.log(doc.data().email);
              document_exists = true;
            }
          });
          if (!document_exists) {
            console.log("Firebase Document does not exsist... Creating one.");
            db.collection("users")
              .orderBy("CreatedTimestamp", "desc")
              .limit(1)
              .get()
              .then((snapshot) => {
                snapshot.docs.forEach((doc) => {
                  //console.log(doc.data().email)
                  lastUser = doc.data().User_ID + 1;
                  //console.log("USER: " + doc.data().User_ID);
                  //console.log(lastUser);
                  //document titles correlate to User UID
                  db.collection("users").doc(this.user.uid).set({
                    User_ID: lastUser,
                    displayName: this.user.displayName,
                    email: this.user.email,
                    signInMethod: "Google",
                    CreatedTimestamp: firebase.firestore.Timestamp.now(),
                  });
                });
              })
              .catch((err) => {
                alert("DOCUMENTS Oops. " + err.message);
              });
          }
        });
      
    },
    guestLogin() {
      firebase
        .auth()
        .signInAnonymously()
        .then(() => {
          this.$router.push("/dashboard");
        });
    },
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        this.$router.push("/dashboard");
      }
    });
  },
};
</script>

<style>
.canvas {
  position: fixed;
  left: 0;
}
</style>