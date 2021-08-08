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
      max-width="600"
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

      <v-card-actions class="justify-center">
        <v-btn class="primary" @click="emailLogin">
          <v-img
            class="mr-2"
            width="20px"
            alt="Email sign-in"
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/mail.svg "
          ></v-img>
          Register
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import firebase from "firebase";
import { ParticlesBg } from "particles-bg-vue";
const isActive = false;


export default {
  name: "Login",
  components: {
    ParticlesBg,
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
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
     submit() {
      if (this.$refs.form.validate()) {
      firebase
        .auth()
        .createUserWithEmailAndPassword(this.email, this.password)
        .then(data => {
          data.user
            .updateProfile({
              displayName: this.name
            })
            .then(() => {});
        })
        .catch(err => {
          this.error = err.message;
        });
    }
  }
  }
};
</script>

<style>

.canvas {
  position: absolute;
  width: 100vw;
  height: 10
  0vh;
}

</style>