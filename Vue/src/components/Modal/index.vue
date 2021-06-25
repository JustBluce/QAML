<!-- Written by Atith Gandhi-->
<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal">
        <header v-if="question_saved" class="modal-header" style="color: green">
          <slot name="header"> Saved !!! </slot>
          <a class="fas fa-times" @click="close" />
        </header>
        <header v-else class="modal-header" style="color: red">
          <slot name="header"> Not Saved !!! </slot>
          <a class="fas fa-times" @click="close" />
        </header>

        <section class="modal-body" v-if="question_saved">
          <slot name="body"> Your question is submitted </slot>
        </section>
        <section class="modal-body" v-else>
          <slot name="body">
            Your question has Easy level difficulty. Please try again.
          </slot>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Modal",
  props: {
    difficulty: {
      type: String,
      default: "Easy",
    },
    question_saved: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    close() {
      this.$store.state.modal.opened = false;
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #ffffff;
  box-shadow: 2px 2px 20px 1px;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  padding: 15px;
  width: 40%;
}
.modal {
  background-color: #fafafa;
  display: flex;
  flex-direction: column;
}
.modal-header {
  padding: 15px;
  display: flex;
}

.modal-header {
  position: relative;
  border-bottom: 1px solid #eeeeee;
  justify-content: space-between;
}

.modal-body {
  position: relative;
  padding: 20px 10px;
}

.fas {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 20px;
  padding: 10px;
  cursor: pointer;
  color: steelblue;
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
</style>
