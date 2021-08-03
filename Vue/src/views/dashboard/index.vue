<template>
  <v-main>
    <Taskbar title="Dashboard" />
    <Profile></Profile>
 





  </v-main>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import Profile from "@/components/auth/profile"

export default {
  name: "Dashboard",
  components: {
    Taskbar,
    Profile,
  },
};
</script>
