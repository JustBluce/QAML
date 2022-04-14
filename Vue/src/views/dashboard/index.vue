<!--
Developers: Jason Liu, Damian Rene, and Cai Zefan
-->

<template>
  <div class="dashboard-container">
    <Taskbar title="Dashboard" />
      
      <v-row no-gutters> 
         <!-- Left SIDE   <draggable tag="v-layout" > -->
        <v-col md=9>
            <v-row no-gutters> 
                <v-col md=4>
                  <!--Blank left Area > -->
                </v-col>
                <v-col md=4>
                    <Profile /> 
                </v-col>
                <v-col md=4>
                     <!--Blank right Area > -->
                </v-col>
            </v-row>

            <v-row no-gutters> 
               <WorkspaceStats/>
                <GenreStats/>
            </v-row>
            
        </v-col>


        <!-- Right SIDE -->
        <!-- Status contians Leaderboards -->
         
        <v-col md=3>
            <Leaderboard/>
        </v-col>
        
      </v-row>

       
      
  </div>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import draggable from "vuedraggable";
import Profile from "@/components/Dashboard/Profile.vue";
import WorkspaceStats from "@/components/Dashboard/WorkspaceStats.vue";
import GenreStats from "@/components/Dashboard/GenreStats.vue"
import Friends from "@/components/Dashboard/Friends.vue";
import Leaderboard from '@/components/Dashboard/Leaderboard.vue';



export default {
  name: "Dashboard",
  components: {
    Taskbar,
    Profile,
    Friends,
    WorkspaceStats,
    GenreStats,
    Leaderboard,
    draggable
   
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