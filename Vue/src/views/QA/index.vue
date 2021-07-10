<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <div id="app">
    <Taskbar />
    <div class="workspaces-container">
      <transition-group type="transition" name="workspaces">
        <div v-for="workspace in workspaces" :key="workspace.id">
          <Workspace :id="workspace.id" />
        </div>
      </transition-group>
    </div>
  </div>
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
      displayUI: "block",
    };
  },
  computed: {
    workspaces() {
      return this.$store.state.workspaces;
    },
  },
};
</script>

<style>
.container {
  border: 0px;
  border-radius: 5px;
  box-sizing: border-box;
  background-color: rgba(241, 241, 241, 0.98);
  padding: 10px;
  margin-top: 10px;
  resize: none;
  outline: none;
  overflow: auto;
  overflow: overlay;
  overflow-wrap: break-word;
}

.workspaces-container {
  position: relative;
  height: calc(100vh - 100px);
  overflow: hidden;
}

.workspaces-enter-active,
.workspaces-leave-active {
  position: relative;
  transition: all 0.3s ease;
  z-index: 1000;
}

.workspaces-enter {
  transform: translate(0, -500px);
}

.workspaces-leave-to {
  opacity: 0;
}

.btn {
  color: steelblue;
  cursor: pointer;
  opacity: 1;
  transition: opacity 0.3s;
}

.btn:hover {
  color: steelblue;
  opacity: 0.7;
}

.btn:active {
  transform: scale(0.9);
}

.fa-minus,
.fa-minus:hover {
  color: #a62c2b;
}

.fa-plus,
.fa-plus:hover {
  color: #296e01;
}

.fa-trash,
.fa-trash:hover {
  color: #888888;
}

.fa-upload {
  color: #ffffff;
}
</style>