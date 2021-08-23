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
      <v-card-title class="text-h3 justify-center">Password Reset</v-card-title>

      <v-form ref="form" class="px-8">
        <v-text-field
          v-model="email"
          label="Email"
          placeholder="Email address to reset password"
          :rules="emailRules"
        ></v-text-field>
      </v-form>

      <v-card-actions class="justify-center pb-4">
        <v-btn class="primary" @click="resetPassword">
          <v-img
            class="mr-2"
            width="20px"
            alt="Password Reset"
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/mail.svg "
          ></v-img>
          Send Reset Email
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import firebase from "firebase";
import { ParticlesBg } from "particles-bg-vue";

export default {
  name: "PReset",
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
    resetPassword() {
      firebase
        .auth()
        .sendPasswordResetEmail(this.email)
        .then(() => {
          alert("Reset Email Sent!");
          // Password reset email sent!
          // ..
        })
        .catch((error) => {
          var errorCode = error.code;
          var errorMessage = error.message;
          // ..
        });
    },
  },
};
</script>