<template>
<div>
  
    <Taskbar title="Dashboard" />
   
 <Profile></Profile>
    
    
   
  
  </div>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import Profile from "@/components/auth/profile"
import { ParticlesBg } from "particles-bg-vue";


export default {
  name: "Dashboard",
  components: {
    Taskbar,
    Profile,
    ParticlesBg
  
  },
};
</script>

<style scoped>
.background{
  
}
</style>
