<template>
  <div>
    <Taskbar title="Workspace Manager" />

    <v-container class="px-16 pt-8">
      <v-text-field
        append-icon="mdi-magnify"
        label="Workspace title"
        v-model="search"
        single-line
      ></v-text-field>
    </v-container>

    <v-container class="workspaceContainer">
      <p v-show="filteredWorkspaces.length == 0" class="py-4 text-center">
        No workspaces
      </p>
      <transition-group
        type="transition"
        name="workspaceCards"
        tag="v-row"
        dense
      >
        <v-col
          v-for="workspace in filteredWorkspaces"
          :key="workspace.id"
          :cols="4"
        >
          <WorkspaceCard :workspace="workspace" />
        </v-col>
      </transition-group>
    </v-container>
  </div>
</template>

<script>
import Taskbar from "@/components/Taskbar";
import WorkspaceCard from "@/components/WorkspaceCard";

export default {
  name: "Workspaces",
  components: {
    Taskbar,
    WorkspaceCard,
  },
  data() {
    return {
      search: "",
    };
  },
  computed: {
    filteredWorkspaces() {
      return this.$store.state.workspaces.filter((workspace) =>
        workspace.title.toLowerCase().includes(this.search.toLowerCase())
      );
    },
  },
};
</script>

<style scoped>
.workspaceContainer {
  height: calc(100vh - 200px);
  overflow: auto;
}

.workspaceCards-move {
  transition: transform 0.3s ease;
}

.workspaceCards-enter-active,
.workspaceCards-leave-active {
  display: none;
  position: absolute;
}
</style>