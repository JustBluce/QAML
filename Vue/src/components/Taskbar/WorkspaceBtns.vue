<!--
Developers: Jason Liu
-->

<template>
  <div>
    <v-btn
      id="createWorkspace"
      color="green"
      class="mr-1"
      icon
      large
      @click="createWorkspace"
    >
      <v-icon>mdi-plus</v-icon>
      <v-tooltip bottom activator="#createWorkspace">
        <span>Create workspace</span></v-tooltip
      >
    </v-btn>

    <v-btn
      id="openWorkspace"
      color="primary"
      class="mr-1"
      icon
      large
      @click="show = true"
    >
      <v-icon>mdi-dock-window</v-icon>
      <v-tooltip bottom activator="#openWorkspace">
        <span>Open workspaces</span>
      </v-tooltip>
    </v-btn>

    <v-btn
      id="closeWorkspaces"
      color="red"
      class="mr-1"
      icon
      large
      @click="closeWorkspaces"
    >
      <v-icon>mdi-close</v-icon>
      <v-tooltip bottom activator="#closeWorkspaces">
        <span>Close all workspaces</span>
      </v-tooltip>
    </v-btn>

    <v-dialog v-model="show" width="400">
      <v-card height="600">
        <v-card-title>
          Open workspaces
          <v-spacer></v-spacer>
          <v-btn icon @click="show = false">
            <v-icon color="red">mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="py-2 px-6">
          <v-text-field
            append-icon="mdi-magnify"
            label="Workspace title"
            v-model="search"
            single-line
          ></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <p v-show="filteredWorkspaces.length == 0" class="py-4 text-center">
          No unopened workspaces found
        </p>
        <v-virtual-scroll
          v-if="filteredWorkspaces.length > 0"
          :bench="2"
          :items="filteredWorkspaces"
          height="450"
          item-height="64"
        >
          <template v-slot:default="{ item }">
            <v-list-item :key="item.id">
              <v-list-item-action>
                <v-btn
                  icon
                  large
                  outlined
                  color="green"
                  @click="$store.commit('addWorkspace', item.id)"
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.title }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
          </template>
        </v-virtual-scroll>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "WorkspaceBtns",
  data() {
    return {
      show: false,
      search: "",
    };
  },
  computed: {
    filteredWorkspaces() {
      return this.$store.state.workspaces.filter(
        (workspace) =>
          workspace.title.toLowerCase().includes(this.search.toLowerCase()) &&
          !this.$store.state.workspace_stack.includes(workspace.id)
      );
    },
  },
  methods: {
    createWorkspace() {
      this.$store.commit("createWorkspace");
    },
    closeWorkspaces() {
      this.$store.state.workspaces.forEach((workspace) =>
        this.$store.commit("closeWorkspace", workspace.id)
      );
    },
  },
};
</script>
