<template>
  <v-toolbar>
    <v-switch
      v-model="$vuetify.theme.dark"
      label="Theme"
      inset
      persistent-hint
    ></v-switch>
  </v-toolbar>
  <!--
  <div class="taskbar-container">
    <div class="taskbar">
      <div class="item-wrapper tabs">
        <div class="item" v-for="workspace in workspaces" :key="workspace.id">
          <a
            :class="[
              'btn',
              workspace_selected === workspace.id ? 'selected' : '',
            ]"
            :title="workspace.title"
            @click="selectWorkspace(workspace.id)"
            >{{ workspace.title }}</a
          >
        </div>
      </div>
      <a class="fas fa-plus btn" @click="addWorkspace" />
        <v-switch
        v-model="$vuetify.theme.dark"
        inset
        persistent-hint
      ></v-switch>
      <div class="item recommended-title">Recommended topics:</div>
      <div class="item-wrapper recommended">
        <div class="item" v-for="rec in recommended" :key="rec">
          <a class="btn" :title="rec" @click="addRecommendedWorkspace(rec)">{{
            rec
          }}</a>
        </div>
        <div class="item" v-show="recommended.length === 0">None</div>
      </div>
    </div>
  </div> -->
</template>

<script>
export default {
  name: "Taskbar",
  computed: {
    workspaces() {
      return this.$store.state.workspaces;
    },
    workspace_selected() {
      return this.$store.state.workspace_stack.slice(-1)[0];
    },
    recommended: {
      get() {
        return this.$store.state.recommended;
      },
      set(value) {
        this.$store.state.recommended = value;
      },
    },
  },
  methods: {
    addWorkspace() {
      this.$store.commit("addWorkspace");
    },
    selectWorkspace(id) {
      this.$store.commit("selectWorkspace", id);
    },
    addRecommendedWorkspace(title) {
      this.recommended = this.recommended.filter((rec) => rec !== title);
      this.$store.commit("addWorkspace", title);
    },
  },
};
</script>

<style scoped>
.taskbar-container {
  height: 50px;
  padding: 8px;
  padding-bottom: 4px;
}

.taskbar {
  display: flex;
  align-items: center;
  background-color: white;
  border: 4px solid steelblue;
  border-radius: 24px;
  box-shadow: 0px 0px 2px black;
  font-size: 24px;
  padding-left: 20px;
  padding-right: 20px;
  height: 100%;
  min-width: 1184px;
}

.fa-plus {
  margin-right: 10px;
}

.item {
  font-size: 18px;
  height: 20px;
  padding-left: 6px;
  padding-right: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-wrapper {
  display: flex;
}

.item-wrapper .item {
  border-left: 2px solid black;
}

.item-wrapper .item:first-child {
  border-left: 0;
}

.item-wrapper .btn {
  color: black;
}

.item-wrapper .btn:hover {
  opacity: 1;
}

.item-wrapper .btn:active {
  opacity: 0.5;
}

.tabs {
  max-width: 70%;
  margin-right: 4px;
}

.selected {
  text-decoration: underline;
  text-decoration-thickness: 2px;
}

.recommended-title {
  font-weight: bold;
  text-align: right;
  flex-grow: 1;
}

.recommended {
  max-width: 25%;
}
</style>