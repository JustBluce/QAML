<!--
Developers: Jason Liu, Damian Rene, and Cai Zefan
-->

<template>
  <div>
    <Taskbar title="Dashboard" />

    <v-container fluid class="dashboard-container">
      <Profile />
      <WorkspaceStats />
      <Leaderboard />
    </v-container>
  </div>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import Profile from "@/components/Dashboard/Profile.vue";
import WorkspaceStats from "@/components/Dashboard/WorkspaceStats.vue";
import Leaderboard from "@/components/Dashboard/Leaderboard.vue";

export default {
  name: "Dashboard",
  components: {
    Taskbar,
    Profile,
    WorkspaceStats,
    Leaderboard,
  },
};
</script>

<style scoped>
.dashboard-container {
  overflow-y: auto;
  height: calc(100vh - 64px);
}
</style>
