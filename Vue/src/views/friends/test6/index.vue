<!--
Developers: Jason Liu and Cai Zefan
-->

<template>
  <div id="app">
    <WidgetMenu />
    <draggable
      v-model="widgets"
      ghost-class="ghost"
      handle=".handle"
      group="widgets"
      @start="drag = true"
      @end="(drag = false), (displayUI = 'block')"
    >
      <transition-group type="transition" name="widgets">
        <div class="fit widget-item" v-for="widget in widgets" :key="widget.id">
          <Widget
            :widget="widget"
            :displayUI="displayUI"
            @mousedown.native="displayUI = 'none'"
            @mouseup.native="displayUI = 'block'"
          />
        </div>
      </transition-group>
    </draggable>
    <Modal
      v-show="showModal"
      :difficulty="getDifficulty"
      :question_saved="getQuestionSaved"
    />
    <Warning_Modal
      v-show="getSimilarityWarning"
      :similar_question="getSimilarQuestion"
    />
  </div>
</template>

<script>
import Widget from "@/components/Widget";
import WidgetMenu from "@/components/WidgetMenu";
import Modal from "@/components/Modal";
import draggable from "vuedraggable"
import Warning_Modal from "@/components/Warning_Modal";

export default {
  components: {
    Widget,
    WidgetMenu,
    Modal,
    draggable,
    Warning_Modal
  },
  data() {
    return {
      drag: false,
      displayUI: "block",
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
      return this.difficulty;
    },
    getQuestionSaved() {
      return this.$store.state.modal.question_saved;
    },
    getSimilarityWarning() {
      return this.$store.state.warning_modal.opened;
    },
    getSimilarQuestion (){
      return this.$store.state.warning_modal.similar_question;
    }
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

.widget-item {
  margin-top: 20px;
  margin-left: 20px;
}

.widgets-move {
  transition: all 0.3s ease;
}

.widgets-enter-active,
.widgets-leave-active {
  transition: all 0.3s ease;
  position: absolute;
}

.widgets-enter,
.widgets-leave-to {
  opacity: 0;
}

.ghost {
  opacity: 0.3;
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
</style>
