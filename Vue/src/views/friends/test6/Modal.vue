<!-- Written by Atith Gandhi-->
<script>
  export default {
    props: {
        difficulty: {
            type: String,
            default: "Easy"
        },
        question_saved: {
            type: Boolean,
            default: false
        }
    },
    name: 'Modal',
    methods: {
      close() {
        this.$emit('close');
      },
    },
  };
</script>
<template>
<transition name="modal-fade">
  <div class="modal-backdrop">
    <div class="modal">
      <header v-if="question_saved" class="modal-header" style="color: green">
        <slot  name="header">
        Saved !!!
        </slot>
        <button
          type="button"
          class="btn-close"
          @click="close"
        >
          x
        </button>
      </header>
      <header v-else class="modal-header" style="color: red">
        <slot  name="header">
        Not Saved !!!
        </slot>
        <button
          type="button"
          class="btn-close"
          @click="close"
        >
          x
        </button>
      </header>
      <section class="modal-body" v-if="question_saved">
        <slot name="body">
          Your question is submitted
        </slot>
       </section>

      <section class="modal-body" v-else>
        <slot name="body">
          Your question has Easy level difficulty. Please try again.
        </slot>
       </section>
      <footer class="modal-footer">
        
        <button
          type="button"
          @click="close"
        >
          Ok
        </button>
      </footer>
    </div>
  </div>
  </transition>
</template>
<style>
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
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
    padding: 15px;
    width: 40%;
  }
    .modal {
        background-color: #FAFAFA;
        display: flex;
        flex-direction: column;
    }
  .modal-header,
  .modal-footer {
    padding: 15px;
    display: flex;
  }

  .modal-header {
    position: relative;
    border-bottom: 1px solid #eeeeee;
    justify-content: space-between;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: column;
    justify-content: flex-end;
  }

  .modal-body {
    position: relative;
    padding: 20px 10px;
  }

  .btn-close {
    position: absolute;
    top: 0;
    right: 0;
    border: none;
    font-size: 20px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    background: transparent;
  }

  .btn-green {
    color: white;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }
</style>
