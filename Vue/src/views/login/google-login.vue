<template>
  <div id="login" class="boxy">
      
      <h1 class="welcome"> Welcome to the Improve QA Interface</h1>
      <h1 class="title" >LOGIN WITH </h1>
     
      <img class="google-icon" src= "@/assets/google.png">
      <br>
      <button @click="googleSignIn" class="social-button" >
          <img  src='@/assets/google-logo.png'>
      </button>
        
    </div>
</template>



<script>

import firebase from "firebase"; 

export default {
    

methods:{
    
    
   googleSignIn: function(){
        
        const provider = new firebase.auth.GoogleAuthProvider();
        firebase.auth().signInWithPopup(provider).then(()=>{
            this.$router.push({ path: '/' })
        }).catch(err =>{
            console.log(err);
        })
        
    }  

}
};

</script>
    

<style scoped>
/* social-button = Small G */

.social-button{
    display: block; 
    margin-left: auto; 
    margin-right: auto;
    width: 95px;
    height: 95px;
    background: rgb(255, 255, 255);
    padding: 10px; 
    border-radius: 100%;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,0.2);
    outline: 0;
    border: 0; 
    
    transition-timing-function: linear;
    transition: width 2s, height 2s,margin-left 2s;
    transition-delay: 0.2s;
    
}
.social-button:hover {
  width: 130px;
  height: 130px;
}

.social-button:active{
    box-shadow: 0 2px 4px 0 rgba(0.0.0.0/1);
}

.social-button img{
    width: 100%;
    height: 100%;
    
    transition-timing-function: linear;
     transition: width 2s, height 2s, margin-left 2s;
     transition-delay: 0.2s;
   
}
.social-button img:hover {
  width: 100px;
  height: 100px;
  
  
}


/* google-icon =  GOOGLE word*/
.google-icon{
   display: block; 
    margin-left: auto; 
    margin-right: auto;
    padding: 20px; 
    width: 40%;
    font-size: 180%;
}
.title{
    margin: auto;
    margin-top: 100px;
    text-align: center;
    font-size: 180%;
    font-family: Georgia, serif;
}
.welcome{
    margin: auto;
    padding: 20px; 
    font-family: Georgia, serif;
    font-size: 180%;
    font-weight: normal;
    text-align: center;
}
.boxy{
    margin-left: 35%;
    margin-top:10%;
    width: 400px;
    height:500px;
    border: 0.2rem solid #676767;
    border-radius: 10px;
    

}

</style>