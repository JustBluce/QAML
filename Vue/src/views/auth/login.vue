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

      <v-card-actions class="justify-center">
        <v-btn class="primary" @click="emailLogin">
          <v-img
            class="mr-2"
            width="20px"
            alt="Email sign-in"
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/mail.svg "
          ></v-img>
          Email login
        </v-btn>
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
          <v-icon class="mr-2" size="20">mdi-account-circle</v-icon>
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
        .then(() => {
          this.$router.push("/dashboard");
        })
        .catch((err) => {
          alert("Oops. " + err.message);
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
  position: absolute;
  left: 0;
}
</style>