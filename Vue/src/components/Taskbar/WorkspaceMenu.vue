<template>
  <v-menu
    offset-y
    rounded
    :close-on-content-click="false"
    style="z-index: 1000"
  >
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" icon>
        <v-icon>mdi-dock-window</v-icon>
      </v-btn>
    </template>

    <v-list>
      <v-list-item>
        <v-btn
          color="green"
          class="mx-auto"
          style="width: 225px"
          text
          outlined
          @click="$store.commit('createWorkspace')"
        >
          Create workspace
        </v-btn>
      </v-list-item>
      <v-list-item>
        <v-btn
          color="primary"
          class="mx-auto"
          style="width: 225px"
          text
          outlined
          @click="show = true"
        >
          Load workspace
        </v-btn>
      </v-list-item>
      <v-list-item>
        <v-btn
          color="red"
          class="mx-auto"
          style="width: 225px"
          text
          outlined
          @click="
            $store.state.workspaces.forEach((workspace) =>
              $store.commit('removeWorkspace', workspace.id)
            )
          "
        >
          Clear all workspaces
        </v-btn>
      </v-list-item>
    </v-list>

    <v-dialog v-model="show" width="400" persistent>
      <v-card height="600">
        <v-card-title>
          Load workspaces
          <v-spacer></v-spacer>
          <v-btn icon @click="show = false">
            <v-icon color="red">mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4 text-center" v-show="workspaces.length == 0">
          No workspaces to load
        </v-card-text>
        <v-virtual-scroll
          v-if="workspaces.length > 0"
          :bench="2"
          :items="workspaces"
          height="500"
          item-height="64"
          class="background"
        >
          <template v-slot:default="{ item }">
            <v-list-item :key="item">
              <v-list-item-action>
                <v-btn
                  icon
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
  </v-menu>
</template>

<script>
export default {
  name: "WorkspaceMenu",
  data() {
    return {
      show: false,
    };
  },
  computed: {
    workspaces() {
      return this.$store.state.workspaces.filter((workspace) => !workspace.tab);
    },
  },
};
</script>
