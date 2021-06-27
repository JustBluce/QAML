import firebase from './firebase';
import store from './store';

firebase.auth().onAuthStateChanged(function(user){
    if(user){
        store.commit('user/USER_DETAILS', user);

    }else{
        store.commit('user/LOGOUT');
    }
})