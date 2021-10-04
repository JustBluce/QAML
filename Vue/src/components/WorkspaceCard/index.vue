<!--
Developers: Jason Liu
-->

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
    <v-card-text class="pt-4 pb-2">
      <strong>Genre:</strong>
      <p class="text">{{ workspace.qa.genre || "none" }}</p>
      <strong>Question:</strong>
      <p class="text">{{ workspace.qa.text || "empty" }}</p>
      <strong>Answer:</strong>
      <p class="text">{{ workspace.qa.answer_text || "empty" }}</p>
    </v-card-text>
    <v-card-actions class="pa-4 pt-0">
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
      <v-btn
        color="primary"
        style="width: 75px"
        text
        outlined
        @click="confirmReset"
      >
        Reset
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon fab small elevation="2" @click="downloadQuestion()">
        <v-icon>mdi-cloud-download</v-icon>
      </v-btn>
      <v-btn class="ml-2" icon fab small elevation="2" @click="confirmDelete">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-card-actions>

    <v-dialog v-model="popup.show" max-width="500">
      <v-card>
        <v-card-title class="text-h5">{{ popup.title }}</v-card-title>
        <v-card-text v-html="popup.text"></v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="popup.show = false">
            Cancel
          </v-btn>
          <v-btn color="red" text @click="popup.action">{{ popup.type }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import fileDownload from "js-file-download";
import jsonFormat from "json-format";

export default {
  name: "WorkspaceCard",
  props: {
    workspace: Object,
  },
  data() {
    return {
      popup: {
        show: false,
        title: "",
        text: "",
        action: null,
      },
    };
  },
  computed: {
    workspace_stack() {
      return this.$store.state.workspace_stack;
    },
  },
  methods: {
    confirmDelete() {
      if (this.workspace.qa.text || this.workspace.qa.answer_text) {
        let self = this;
        this.popup = {
          show: true,
          type: "Delete",
          title: "Confirm workspace deletion",
          text: `Are you sure you want to delete <strong>${self.workspace.title}</strong>?`,
          action: function () {
            self.$store.commit("deleteWorkspace", self.workspace.id);
            self.popup.show = false;
          },
        };
      } else {
        this.$store.commit("deleteWorkspace", this.workspace.id);
      }
    },
    confirmReset() {
      if (this.workspace.qa.text || this.workspace.qa.answer_text) {
        let self = this;
        this.popup = {
          show: true,
          type: "Reset",
          title: "Confirm workspace reset",
          text: `Are you sure you want to reset <strong>${self.workspace.title}</strong> (including question, answer, and genre)?`,
          action: function () {
            self.$store.commit("resetWorkspace", self.workspace.id);
            self.popup.show = false;
          },
        };
      } else {
        this.$store.commit("resetWorkspace", this.workspace.id);
      }
    },
    downloadQuestion() {
      fileDownload(
        jsonFormat({
          Question: this.workspace.qa.text,
          Answer: this.workspace.qa.answer_text,
          Genre: this.workspace.qa.genre,
        }),
        `${this.workspace.title}.json`
      );
    },
  },
};
</script>

<style scoped>
.text {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}
</style>