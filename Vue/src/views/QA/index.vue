<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <v-main id="app">
    <Taskbar/>
    <v-sheet class="workspaces-container background">
      <transition-group type="transition" name="workspaces">
        <Workspace
          v-for="workspace_id in workspace_stack"
          :key="workspace_id"
          :id="workspace_id"
        />
      </transition-group>
    </v-sheet>
  </v-main>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import Workspace from "@/components/Workspace";
import draggable from "vuedraggable";

export default {
  components: {
    Taskbar,
    Workspace,
    draggable,
  },
  data() {
    return {
      drag: false,
    };
  },
  computed: {
    workspace_stack() {
      return this.$store.state.workspace_stack;
    },
  },
};
</script>

<style>
html {
  overflow-y: hidden;
}

.workspaces-container {
  position: relative;
  height: calc(100vh - 64px);
  overflow: hidden;
}

.workspaces-enter-active,
.workspaces-leave-active {
  position: relative;
  transition: all 0.3s ease;
  height: 100%;
  z-index: 1000;
}

.workspaces-enter {
  transform: translate(0, -500px);
}

.workspaces-leave-to {
  opacity: 0;
  filter: contrast(0);
}

.ghost {
  opacity: 0.3;
}
</style>