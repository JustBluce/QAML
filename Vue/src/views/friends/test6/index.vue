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
import { VueEditor } from "vue2-editor";
import Widget from "@/components/Widget";
import Modal from "@/components/Modal";
import draggable from "vuedraggable";

export default {
  components: {
    VueEditor,
    Widget,
    Modal,
    draggable,
  },
  data() {
    return {
      widgets: [],
      drag: false,
    };
  },
  computed: {
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
      this.widgets = this.widgets.filter((widget) => widget.id !== id);
    },
  },
  created() {
    this.widgets = [
      {
        id: 0,
        title: "QA1",
        type: "QA",
        removable: false,
      },
      {
        id: 1,
        title: "QA2",
        type: "QA",
        removable: true,
      },
      {
        id: 2,
        title: "Timer",
        type: "Timer",
        removable: true,
      },
    ];
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
  transition: transform 0.5s;
}

.ghost {
  overflow: hidden;
  opacity: 0.5;
  background: #c8ebfb;
}
</style>
