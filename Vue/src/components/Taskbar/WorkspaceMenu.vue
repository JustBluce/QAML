<template>
  <v-menu offset-y rounded :close-on-content-click="false">
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
          @click="true"
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
  </v-menu>
</template>