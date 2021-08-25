<template>
  <v-app>
    <!-- display nav bar -->
    <div v-if="showBar.includes($route.name)">
      <nav-bar />
    </div>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "@/views/NavBar";

export default {
  name: "App",
  components: {
    NavBar,
  },
  data() {
    return {
      showBar: ["Login", "Register", "About", "Tutorial"],
    };
  },
};
</script>
