<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <v-main>
    <Taskbar />
    <v-sheet class="workspaces-container">
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
  overflow: hidden;
}

.v-data-table__expanded.v-data-table__expanded__content {
  box-shadow: none !important;
}

.v-data-table-header,
.v-data-table__empty-wrapper {
  background-color: var(--v-background-base) !important;
}

.workspaces-container {
  position: relative;
  overflow: hidden;
  height: calc(100vh - 112px);
}

.workspaces-enter-active,
.workspaces-leave-active {
  position: relative;
  height: 100%;
  z-index: 1000;
}

.workspaces-enter {
  transform: translate(0, -100vh);
}

.workspaces-enter-active {
  transition: all 0.3s ease;
}

.workspaces-leave-to {
  transform: translate(0, -200vh);
}

.workspaces-leave-active {
  transition: all 0.5s ease;
}

.ghost {
  opacity: 0.3;
}
</style>