<template>
    <section>
        
        <h1 class="title">Profile</h1>
        <div class="card horizontal"  v-if="user">
            
            <div class="card-image" style="margin-top:25px;margin-left:10px;">
                <img
                    :src="user.photoURL"
                    style="width:75px;height:75px;border-radius:50%;border:4px solid #333"
                />
            </div>
            <div class="card-stacked">
                <div class="card-content">
                    <p>
                        Name:
                        <strong>{{user.displayName}}</strong>
                        <br />Email:
                        <strong>{{user.email}}</strong>
                        <!--<br />Uid:
                        <strong>{{user.uid}}</strong> -->
                        <br />Provider:
                        <strong class="teal-text">{{user.providerData[0].providerId}}</strong>
                    </p>
                    
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import firebase from "firebase";
export default {
    methods:{
        updateUserProfile(){
        // [START auth_update_user_profile]
        const user = firebase.auth().currentUser;

        user.updateProfile({
            photoURL: user.photoURL
        }).then(() => {
            alert("yay")
            // Update successful
            // ...
        }).catch((error) => {
            alert(error);
            // An error occurred
            // ...
        });
        }
    },


    data() {
        return {
            user: null
        };
    },
    
    created() {
        firebase.auth().onAuthStateChanged(user => {
            if (user) {
                this.user = user;
            
            }
        });
    }

};

</script>

<style scoped>
.horizontal{
    min-width:100px; 
    max-width:350px;
    max-height:300px; 
    padding: 5px;
    margin-left: 5%;
    border-radius: 20px;
    border: 2px solid black;
}
.title{
    margin-left: 5%;
}
.card-stacked{
    text-align:center;
}
.card-image{
    text-align:center;
}
</style>