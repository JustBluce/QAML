<!--
Developer: Atith Gandhi
-->

<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal">
        <header class="modal-header" style="color: red">
          <slot name="header"> Warning !!! </slot>
          <a class="fas fa-times btn" @click="close" />
        </header>
        

        <section class="modal-body" style="color: green">
          <slot name="body"> Your question is similar to the below given question. Please rewrite it again: </slot>
        </section>
        <section class="modal-body" >
          <slot name="body">
            {{similar_question}}
          </slot>
        </section>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Warning_Modal",
  props: {
    similar_question: {
      type: String,
      default: " ",
    }
  },
  methods: {
    close() {
      this.$store.state.warning_modal.opened = false;
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
  border-radius: 5px;
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

.btn {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 20px;
  padding: 10px;
}
</style>
