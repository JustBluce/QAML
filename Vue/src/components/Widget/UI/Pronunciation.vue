<!--
Developer: Damien Rene and Jason Liu
-->

<template>
  <div>
    <select class="container" v-model="qa_id">
      <option v-if="qa_widgets.length == 0" :value="qa_id">
        Please create a QA widget
      </option>
      <option
        v-for="qa_widget in qa_widgets"
        :key="qa_widget.id"
        :value="qa_widget.id"
      >
        {{ qa_widget.title }}
      </option>
    </select>
    <div readonly class="container output" @click="clickMethod">
      <div class="placeholder" v-show="!text">Please enter your question</div>
      <Highlighter
        :style="{ color: 'black' }"
        highlightClassName="highlight"
        :searchWords="keywords"
        :autoEscape="true"
        :textToHighlight="text"
      />
    </div>
  </div>
</template>

<script>
import Highlighter from "vue-highlight-words";
export default {
  name: "Pronunciation",
  props: {
    workspace_id: Number,
    widget_id: Number,
  },
  components: {
    Highlighter,
  },
  data() {
    return {
      words: "and or the quick",
    };
  },
  computed: {
    qa_id: {
      get() {
        return this.$store.getters.widget(this.workspace_id, this.widget_id)
          .qa_id;
      },
      set(value) {
        this.$store.commit("updateWidget", {
          workspace_id: this.workspace_id,
          payload: { id: this.widget_id, qa_id: value },
        });
      },
    },
    qa_widgets() {
      let qa_widgets = this.$store.getters
        .workspace(this.workspace_id)
        .widgets.filter((widget) => widget.type === "QA");
      if (
        qa_widgets.length > 0 &&
        !qa_widgets.some((widget) => widget.id === this.qa_id)
      ) {
        this.qa_id = qa_widgets[0].id;
      }
      return qa_widgets;
    },
    text() {
      if (this.qa_widgets.length === 0) {
        return "";
      }
      return this.$store.getters.widget(this.workspace_id, this.qa_id).text;
    },
    keywords() {
      return this.words.split(" ");
    },
  },
  methods: {
    clickMethod() {
      //window.location.href = 'https://www.google.com/';
    },
  },
};
</script>

<style scoped>
select {
  cursor: pointer;
  opacity: 1;
  transition: opacity 0.3s;
}

select:hover {
  opacity: 0.7;
}

.output {
  cursor: default;
  overflow: auto;
  height: 128px;
}

.placeholder {
  color: #757575;
}

.highlight {
  background-color: #c8ebfb;
}
</style>