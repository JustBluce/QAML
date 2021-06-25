<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <div id="app">
    <draggable
      v-model="widgets"
      ghost-class="ghost"
      handle=".handle"
      @start="drag = true"
      @end="drag = false"
    >
      <transition-group type="transition" name="flip-list">
        <div class="fit" v-for="widget in widgets" :key="widget.id">
          <Widget :widget="widget" @delete-widget="deleteWidget" />
        </div>
      </transition-group>
    </draggable>
    <Modal
      v-show="showModal"
      :difficulty="getDifficulty"
      :question_saved="getQuestionSaved"
    />
  </div>
</template>

<script>
import Widget from "@/components/Widget";
import Modal from "@/components/Modal";
import draggable from "vuedraggable";

export default {
  components: {
    Widget,
    Modal,
    draggable,
  },
  data() {
    return {
      drag: false,
    };
  },
  computed: {
    widgets: {
      get() {
        return this.$store.state.widgets;
      },

      set(widgets) {
        this.$store.state.widgets = widgets;
      },
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
  methods: {
    deleteWidget(id) {
      this.$store.commit("deleteWidget", id);
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
  margin-top: 20px;
  margin-left: 20px;
}

.flip-list-move {
  transition: transform 0.3s;
}

.ghost {
  overflow: hidden;
  opacity: 0.5;
  background: #c8ebfb;
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
}
</style>
