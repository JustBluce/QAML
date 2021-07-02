<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <div id="app">
    <div v-for="workspace in workspaces" :key="workspace.id">
      <Workspace :id="workspace.id" />
    </div>
    <Modal
      v-show="showModal"
      :difficulty="getDifficulty"
      :question_saved="getQuestionSaved"
    />
  </div>
</template>

<script>
import Workspace from "@/components/Workspace";
import Modal from "@/components/Modal";
import draggable from "vuedraggable";

export default {
  components: {
    Workspace,
    Modal,
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
    showModal() {
      return this.$store.state.modal.opened;
    },
    getDifficulty() {
      return this.$store.state.modal.difficulty;
    },
    getQuestionSaved() {
      return this.$store.state.modal.question_saved;
    },
  },
};
</script>

<style>
.fit {
  width: -webkit-fit-content;
  height: -webkit-fit-content;
  width: -moz-fit-content;
  height: -moz-fit-content;
}

.container {
  border: 100px;
  border-radius: 5px;
  box-sizing: border-box;
  background-color: rgba(241, 241, 241, 0.98);
  width: 800px;
  padding: 10px;
  margin-top: 10px;
  resize: none;
  outline: none;
  overflow: auto;
  overflow: overlay;
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
</style>