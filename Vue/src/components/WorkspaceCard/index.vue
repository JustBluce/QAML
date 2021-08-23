<template>
  <v-card class="ma-2" style="border-radius: 16px" elevation="4">
    <v-card-title class="background">
      <p class="text mb-0">{{ workspace.title }}</p>
      <v-spacer></v-spacer>
      <v-btn
        icon
        @click="
          $store.commit('addWorkspace', workspace.id);
          $router.push('/qa');
        "
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text class="pt-4 pb-0">
      <strong>Genre:</strong>
      <p class="text">{{ workspace.qa.genre || "none" }}</p>
      <strong>Question:</strong>
      <p class="text">{{ workspace.qa.text || "empty" }}</p>
      <strong>Answer:</strong>
      <p class="text">{{ workspace.qa.answer_text || "empty" }}</p>
    </v-card-text>
    <v-card-actions class="pa-4">
      <v-btn
        v-if="workspace_stack.includes(workspace.id)"
        color="red"
        style="width: 75px"
        text
        outlined
        @click="$store.commit('closeWorkspace', workspace.id)"
      >
        Close
      </v-btn>
      <v-btn
        v-else
        color="green"
        style="width: 75px"
        text
        outlined
        @click="$store.commit('addWorkspace', workspace.id)"
      >
        Open
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon fab small elevation="2" @click="confirm">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-card-actions>

    <v-dialog v-model="popup" max-width="500">
      <v-card>
        <v-card-title class="text-h5">
          Confirm workspace deletion
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ workspace.title }}</strong
          >?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="popup = false">
            Cancel
          </v-btn>
          <v-btn
            color="red"
            text
            @click="$store.commit('deleteWorkspace', workspace.id)"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  name: "WorkspaceCard",
  props: {
    workspace: Object,
  },
  data() {
    return {
      popup: false,
    };
  },
  computed: {
    workspace_stack() {
      return this.$store.state.workspace_stack;
    },
  },
  methods: {
    confirm() {
      if (this.workspace.qa.text || this.workspace.qa.answer_text) {
        this.popup = true;
      } else {
        this.$store.commit("deleteWorkspace", this.workspace.id);
      }
    },
  },
};
</script>

<style scoped>
.text {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>