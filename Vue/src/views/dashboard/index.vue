<!--
Developers: Jason Liu, Damian Rene, and Cai Zefan
-->

<template>
  <div class="dashboard-container">
    <Taskbar title="Dashboard" />
  
   
      <v-row no-gutters>
        <draggable tag="v-layout" >
          
          <v-col md=4 >
        <WorkspaceStats/>
        </v-col>

        <v-col md=4 >
        <Profile />  
        </v-col>

        <v-col md=4 >
        <GenreStats/>
        </v-col>
        </draggable>
        </v-row>

         
       <Leaderboard />
      

  </div>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import draggable from "vuedraggable";
import Profile from "@/components/Dashboard/Profile.vue";
import WorkspaceStats from "@/components/Dashboard/WorkspaceStats.vue";
import Leaderboard from "@/components/Dashboard/Leaderboard.vue";
import GenreStats from "@/components/Dashboard/GenreStats.vue"


export default {
  name: "Dashboard",
  components: {
    Taskbar,
    Profile,
    
    WorkspaceStats,
    GenreStats,
    Leaderboard,
    draggable,
  },
  data() {
    return {
     
      drag: false, 
     
      dragging: false
    };
  },
  computed: {
    dashboardArray: {
        get() {
            return this.$store.state.dashboardArray;
        },
        set(value) {
            this.$store.commit('updateDashboardArray', value)
        }
    }
},
};
</script>

<style scoped>
.dashboard-container {
  overflow-y: auto;
  height: calc(100vh);
  
}
</style>
