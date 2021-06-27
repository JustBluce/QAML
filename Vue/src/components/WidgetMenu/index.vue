<!--
Developer: Jason Liu
-->

<template>
  <div class="widget-menu">
    <div class="btn-container">Add Widget <a class="fas fa-plus" /></div>
    <div class="container">
      <div
        v-for="widget_type in widget_types"
        class="fit widget-type-item"
        :key="widget_type"
        @click="addWidget(widget_type)"
      >
        {{ widget_type }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WidgetMenu",
  data() {
    return {
      widget_types: this.$store.state.widget_types,
    };
  },
  methods: {
    addWidget(type) {
      this.$store.commit("addWidget", type);
    },
  },
};
</script>

<style scoped>
.widget-menu {
  display: flex;
  flex-direction: column;
  float: right;
  margin-right: 30px;
}

.btn-container {
  text-align: center;
  font-size: 24px;
  border: 2px solid steelblue;
  border-radius: 20px;
  padding: 10px;
  cursor: pointer;
}

.fa-plus {
  color: #296e01;
}

.container {
  overflow: hidden;
  visibility: hidden;
  max-height: 0px;
  margin-top: 0px;
  width: auto;
  transition: max-height 0.3s, visibility 0s 0.3s linear;
}

.widget-menu:hover .container {
  visibility: visible;
  max-height: 150px;
  transition: max-height 0.3s, visibility 0s 0s linear;
}

.widget-type-item {
  font-size: 18px;
  cursor: pointer;
}
</style>