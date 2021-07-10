<template>
  <div class="taskbar">
    <a class="fas fa-plus btn" @click="addWorkspace" />
  </div>
</template>

<script>
export default {
  name: "Taskbar",
  methods: {
    addWorkspace() {
      this.$store.commit("addWorkspace");
    }
  }
};
</script>

<style scoped>
.taskbar {
  display: flex;
  align-items: center;
  height: 50px;
  background-color: #304156;
  font-size: 24px;
  padding-left: 20px;
  padding-right: 20px;
}
</style>