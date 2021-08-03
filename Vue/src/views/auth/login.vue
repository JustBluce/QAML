<template>
<div>
    <particles-bg type="cobweb" :bg="true" />

    <div class="box" >
        
        <h1>Login </h1> 
        <section id="firebaseui-auth-container"></section>
    </div>
   
    </div>
</template>

<script>
import firebase from "firebase";
import * as firebaseui from "firebaseui";
import "firebaseui/dist/firebaseui.css";

import { ParticlesBg } from "particles-bg-vue";

export default {
    name: "Login",
    components: {
    ParticlesBg
  },
  methods: {
    uiShown: function() {
      // The widget is rendered.
      // Hide the loader.
      document.getElementById('loader').style.display = 'none';
    }

  },
    data() {
        return {};
    },

    mounted() {
        let ui = firebaseui.auth.AuthUI.getInstance();
        if (!ui) {
            ui = new firebaseui.auth.AuthUI(firebase.auth());
        }
        var uiConfig = {
            signInSuccessUrl: "/dashboard", // This redirect can be achived by route using callback.
            signInFlow: "popup",
            signInOptions: [
                firebase.auth.GithubAuthProvider.PROVIDER_ID,,
                firebase.auth.GoogleAuthProvider.PROVIDER_ID,
                firebase.auth.EmailAuthProvider.PROVIDER_ID
            ]
        
        };
        ui.start("#firebaseui-auth-container", uiConfig);
    }
    
};
</script>

<style>

.main-container {
    min-height: 100%;
    transition: margin-left .28s;
    position: relative;
  }
  .box{
    text-align:center;
     
    background: rgb(216, 216, 216);
    height: 300px;
    width: 400px;
    padding: 5px;
    margin: auto;
    margin-top: 10%;
    border-radius: 20px;
    border: 2px solid black;
}

</style>