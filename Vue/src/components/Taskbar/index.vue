<template>
  <div class="taskbar-container">
    <div class="taskbar">
      <a class="fas fa-plus btn" @click="addWorkspace" />
    </div>
  </div>
</template>

<script>
export default {
  name: "Taskbar",
  methods: {
    addWorkspace() {
      this.$store.commit("addWorkspace");
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
}
</style>