<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal">
        <header class="modal-header">
          <slot name="header">{{ modal.header }}</slot>
          <a class="fas fa-times btn" @click="close" />
        </header>
        <section class="modal-body">
          <slot name="body">{{ modal.body }}</slot>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Modal",
  computed: {
    modal() {
      return this.$store.state.modal;
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
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter,
.modal-fade-leave-to {
  opacity: 0;
}

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
  z-index: 100;
}

.modal {
  border-radius: 5px;
  box-shadow: 2px 2px 20px 1px;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  padding: 15px;
  width: 40%;
  background-color: #fafafa;
  display: flex;
  flex-direction: column;
}

.modal-header {
  font-weight: bold;
  font-size: 24px;
  padding: 15px;
  display: flex;
  position: relative;
  border-bottom: 1px solid #eeeeee;
  justify-content: space-between;
}

.modal-body {
  font-size: 18px;
  position: relative;
  padding: 15px;
}

.btn {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 20px;
  padding: 10px;
}
</style>
