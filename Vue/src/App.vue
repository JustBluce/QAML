<template>
  <div id="app">
    <!-- display nav bar -->
    <nav-bar v-if="this.$route.name === 'Login' " ></nav-bar>
    <nav-bar v-if="this.$route.name === 'Register' " ></nav-bar>
    <nav-bar v-if="this.$route.name === 'About' " ></nav-bar>

    <router-view />
  </div>
</template>

<script>
import NavBar from '@/views/NavBar'

export default {
  name: 'App',
  components: {
    NavBar
  }
}

</script>
