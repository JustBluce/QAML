<!-- Login Page: Damian Rene--> 
<template>
<div>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">
    
    <particles-bg type="cobweb" :bg="true" />
    
    <div class="box" >
        <form @submit.prevent="emailLogin">
            <div class="title">
                Login 
            </div>

            <div class="form-group">
                <label class="labels">Email address</label>
                <input v-model="email" type="email"  placeholder="Email address..."  class="form-control " />
            </div>

            <div class="form-group">
                <label class="labels">Password</label>
                <input v-model="password" type="password"  placeholder="Password..." class="form-control " />
            </div>

             <div class="col s12 m6 offset-m3 center-align">
            <button  class="email-button" style="margin-top:5%;" >
                    <div class="left">
                        <img width="20px"  alt="Email sign-in" 
                        src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/mail.svg " />
                        </div>

                    <p class="button-text">
                     Login with Email
                     </p>
                </button> 
                </div>

        </form>

        <div class="col s12 m6 offset-m3 center-align">
            <!--  Email button --> 
                

                <div style="margin-top: 5px; margin-bottom:20px;">
                    or
                    </div>

            <!-- Google Button -->
            <button @click="socialLogin" class="google-button" >
                <div class="left">
                    <img width="20px" alt="Google sign-in" 
                        src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" />
                </div>

                <p class="button-text">
                    Login with Google
                </p>
                </button>
                

                <div>
                </div>
        </div>
    </div>      
    </div>
</template>

<script>
import firebase from "firebase";
import { ParticlesBg } from "particles-bg-vue";

export default {
    name: "Login",
    components: {
    ParticlesBg
  },
  data() {
        return {
            email: '',
            password: '',
        };
    },
  methods: {
     socialLogin(){
         const provider = new firebase.auth.GoogleAuthProvider();
         firebase.auth().signInWithPopup(provider).then((result) =>{
             this.$router.replace('Dashboard');

         }).catch((err) => {
             alert('Oops. ' + err.message)
         })
     },
     emailLogin(){
       firebase
      .auth()
      .signInWithEmailAndPassword(this.email, this.password)
      .then(() => {
        this.$router.push('/dashboard');
      })
      .catch(error => {
        alert(error.message);
      });
  },
     
  },

    data() {
        return {};
    },
    
};
</script>

<style>
.left{ 
    margin-left: 10px;
    margin-right: 10px;
}
.button-text{
    margin-top: 2%;
}
.google-button{
    background: white;
    font-size: 14px;
    font-weight: 500;
    padding: 5px;
    border-radius: 2px;
    width: 190px;
    height: 40px;
    text-align: left;
    font-family: Roboto,Helvetica,Arial,sans-serif;
    box-shadow: 0 0 8px 0 rgba(0,0,0,0.25);
}
.google-button:hover{
    box-shadow: 5px 5px 8px rgba(0,0,0,0.25);
}
.google-button:focus{
    background:white;
}
.email-button{
    background: #db4437;
    color: white;
    font-size: 14px;
    font-weight: 500;
    padding: 5px;
    border-radius: 2px;
    width: 190px;
    height: 40px;
    text-align: left;
    font-family: Roboto,Helvetica,Arial,sans-serif;
    box-shadow: 0 0 8px 0 rgba(0,0,0,0.25);
    
}
.email-button:hover{
    box-shadow: 5px 5px 8px rgba(0,0,0,0.25);
}
.email-button:focus{
    background:#db4437;
}
.title{
    margin-top: 10px;
    margin-bottom: 10px;
    text-align: center;
    font-family: Roboto,Helvetica,Arial,sans-serif;
    font-size: 60px;
    font-weight: 100;

}
.main-container {
    min-height: 100%;
    transition: margin-left .28s;
    position: relative;
  }
  .box{
    
    background: rgb(216, 216, 216);
    height: 500px;
    width: 500px;
    padding: 5px;
    margin: auto;
    margin-top: 10%;
    border-radius: 20px;
    border: 2px solid black;
   
}
.form-control:focus {
  border-color: #2554FF;
  box-shadow: none;
}
.form-group{
    font-family: Roboto,Helvetica,Arial,sans-serif;
    font-size: 14px;
    font-weight: 500;
    text-align: left;
    margin-left: 20px;
    margin-right: 20px;
}
.labels{
    color: black;
    font-family: Roboto,Helvetica,Arial,sans-serif;
    font-size: 20px;
    font-weight: 500;
    margin-left: 10px;
   
}
.form-control{
    
}


</style>