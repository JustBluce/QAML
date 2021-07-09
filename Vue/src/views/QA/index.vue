<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <div id="app">
    <div v-for="workspace in workspaces" :key="workspace.id">
      <Workspace :id="workspace.id" />
    </div>
  </div>
</template>

<script>
import Workspace from "@/components/Workspace";
import draggable from "vuedraggable";

export default {
  components: {
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
  color: #FFFFFF;
}
</style>