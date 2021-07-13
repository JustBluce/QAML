<template>
  <div class="taskbar-container">
    <div class="taskbar">
      <a class="fas fa-plus btn" @click="addWorkspace" />
      <div class="recommended recommended-title">Recommended topics:</div>
      <div class="recommended" v-show="recommended.length === 0">None</div>
      <div
        class="recommended btn"
        v-for="rec in recommended"
        :key="rec"
        @click="addRecommendedWorkspace(rec)"
      >
        {{ rec }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Taskbar",
  computed: {
    recommended: {
      get() {
        return this.$store.state.recommended;
      },
      set(value) {
        this.$store.state.recommended = value;
      },
    },
  },
  methods: {
    addWorkspace() {
      this.$store.commit("addWorkspace");
    },
    addRecommendedWorkspace(title) {
      this.recommended = this.recommended.filter((rec) => rec !== title);
      this.$store.commit("addWorkspace", title);
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

.recommended {
  border-right: 2px solid black;
  font-size: 18px;
  float: right;
  padding-left: 4px;
  padding-right: 4px;
  color: black;
}

.recommended:hover {
  color: black;
}

.recommended-title {
  font-weight: bold;
  border-right: 0;
  flex-grow: 1;
  text-align: right;
}

.recommended:last-of-type {
  border-right: 0;
}
</style>