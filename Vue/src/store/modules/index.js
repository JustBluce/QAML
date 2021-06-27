import firebase from 'firebase';

const state = {
  userProfile: {},
  loggedIn: false
};

const getters = {
  userProfile: ({userProfile}) => userProfile,
  loggedIn: ({loggedIn}) => loggedIn
};

const mutations = {
  USER_DETAILS(state, userProfile) {
    state.loggedIn = true;    
    state.userProfile = {
      name: userProfile.displayName,
      picture: userProfile.photoURL
    };
  },
  LOGOUT(state) {
    state.loggedIn = false;
    state.userProfile = {};
  }
};

const actions = {
  async login(store) {

    if (store.state.loggedIn)
      return;

    const provider = new firebase.auth.GoogleAuthProvider();
    try {
      await firebase.auth().signInWithPopup(provider);
    } catch(error) {
      console.log(error);
    }
  },

  async logout() {
    try {
      await firebase.auth().signOut();
    } catch(error) {
      console.log(error);
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};