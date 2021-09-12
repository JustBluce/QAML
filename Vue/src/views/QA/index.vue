<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <div>
    <Taskbar title="QA Interface" :qa="true" />
    <v-container fluid class="workspaces-container">
      <transition-group type="transition" name="workspaces">
        <Workspace
          v-for="workspace_id in workspace_stack"
          :key="workspace_id"
          :id="workspace_id"
        />
      </transition-group>
      <div
        v-if="workspace_stack.length == 0"
        style="height: 100%; opacity: 0.7"
      >
        <v-row dense align="end" justify="center" style="height: 50%">
          <v-icon size="400">mdi-tab-plus</v-icon>
        </v-row>
        <v-row dense align="start" justify="center" style="height: 50%">
          <p class="text-h4 text--secondary">
            Click "<span style="color: var(--v-green-base); font-weight: bold"
              >+</span
            >" to create a workspace
          </p>
        </v-row>
      </div>
    </v-container>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import Taskbar from "@/components/Taskbar";
import Workspace from "@/components/Workspace";

export default {
  name: "QA",
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
.workspaces-container {
  position: relative;
  overflow: hidden;
  height: calc(100vh - 100px);
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