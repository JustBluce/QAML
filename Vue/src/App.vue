<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex';
  
  export default {
    name: 'app',
    computed: {
      ...mapGetters('user', {
        userProfile: 'userProfile',
        loggedIn: 'loggedIn'
      })
    },
    methods: {
      ...mapActions('user', {
        login: 'login',
        logout: 'logout'
      })
    }
  };
</script>