<!--
Developer: Jason Liu
-->

<template>
  <div class="container">
    <h2 ref="header">
      <a class="fas fa-bars handle" @mousedown="hideWidget" />
      {{ widget.title }}
      <a
        v-show="widget.removable"
        class="fas fa-times"
        @click="$emit('delete-widget', widget.id)"
      />
      <a v-show="expanded" class="fas fa-minus" @click="toggleWidget" />
      <a v-show="!expanded" class="fas fa-plus" @click="toggleWidget" />
    </h2>
    <div
      class="widget-container"
      ref="widgetContainer"
      :style="{
        maxHeight: expanded ? widget.maxHeight : '0px',
        opacity: expanded ? '1' : '0',
      }"
    >
      <QA v-if="widget.type === 'QA'" :id="widget.id" />
      <Timer v-if="widget.type === 'Timer'" :end="getEnd()" />
      <Pronunciation v-if="widget.type === 'Pronunciation'" question_id="0" />
    </div>
  </div>
</template>

<script>
import QA from "./QA";
import Timer from "./Timer";
import Pronunciation from "./Pronunciation";

export default {
  name: "Widget",
  props: {
    widget: Object,
  },
  components: {
    QA,
    Timer,
    Pronunciation,
  },
  data() {
    return {
      expanded: true,
      widget_width: 0,
    };
  },
  methods: {
    toggleWidget() {
      this.$refs.widgetContainer.style.display = "block";
      this.expanded = !this.expanded;
    },
    hideWidget() {
      if (!this.expanded) {
        if (this.$refs.widgetContainer.offsetWidth) {
          this.$refs.header.style.width =
            this.$refs.widgetContainer.offsetWidth + "px";
        }
        this.$refs.widgetContainer.style.display = "none";
      }
    },
    getEnd() {
      return new Date("June 27, 2021 12:00:00").getTime();
    },
  },
};
</script>

<style scoped>
h2 {
  margin: 0px;
}

.fas {
  float: right;
  color: steelblue;
  cursor: pointer;
  margin-left: 10px;
  opacity: 1;
  transition: opacity 0.3s;
}

.fas:hover {
  color: steelblue;
  opacity: 0.7;
}

.fas:active {
  transform: scale(0.9);
}

.fa-bars {
  margin-left: 0px;
  margin-right: 5px;
  float: none;
}

.fa-minus,
.fa-minus:hover {
  color: #a62c2b;
}

.fa-plus,
.fa-plus:hover {
  color: #296e01;
}

.container {
  border: 2px solid steelblue;
  border-radius: 5px;
  padding: 30px;
  margin: 0px;
}

.widget-container {
  overflow: hidden;
  transition: max-height 0.5s linear 0s, opacity 0.4s linear 0.1s;
}
</style>