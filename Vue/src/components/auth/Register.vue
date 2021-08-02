<template>
<div class="form-group--error">
  <v-container  >
    <v-layout row wrap>
      <v-flex>
          
        <h1>Register</h1>
        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
          >
          <v-text-field 
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            :rules="passwordRules"
            label="Password"
            required
            :append-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
            :type="passwordShow ? 'text' : 'password'"
             @click:append="passwordShow = !passwordShow"
          ></v-text-field>

          <v-text-field
            v-model="confirmPassword"
            label="confirm Password"
            :rules="passwordRules"
            :type="passwordShow ? 'text' : 'password'"
            required
             @click:append="confirmPasswordShow = !confirmPasswordShow"
          ></v-text-field>

          <v-btn
            :disabled="!valid"
            color="success"
            @click="validate"
          >
            Register
          </v-btn>

          <v-btn
            color="error"
            @click="reset"
          >
            Reset Form
          </v-btn>
        </v-form>
      </v-flex>
    </v-layout>
  </v-container>
  </div>
</template>

<script>

import { required, minLength, between , email} from 'vuelidate/lib/validators'
import Taskbar from "@/components/Taskbar";


export default {
    
  data: () => ({
    passwordShow: false,
    confirmPasswordShow: false,
    valid: true,
    email: '',
    password: '',
    confirmPassword: ''
  }),
  methods: {
    validate () {
      if (this.$refs.form.validate()) {
        this.snackbar = true
        this.registerWithFirebase()
      }
    },
    reset () {
      this.$refs.form.reset()
    },
    registerWithFirebase () {
      const user = {
        email: this.email,
        password: this.password
      }
      this.$store.dispatch('signUpAction', user)
    }
  }
}
</script>

<style scoped>
.title{

}
</style>