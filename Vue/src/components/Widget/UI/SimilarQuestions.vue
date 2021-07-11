<!--
Developers: Atith Gandhi, Raj Shah and Jason Liu
-->

<template>
  <div class="similar-container">
  
                
  
    <div v-for="(val, index) in getTop5_similar_questions[1]">
      <div class="tab__header">
          <a href="#" class="tab__link p-4 block bg-blue-dark hover:bg-blue-darker no-underline text-white border-b-2 border-white flex justify-between" @click.prevent="toggle(index)">
              <br>{{index + 1}}.{{val['answer']}} 
              <span class="down-Arrow" v-show="!active[index]">&#9660;</span>
              <span class="up-Arrow" v-show="active[index]">&#9650;</span>
          </a>
      </div>
      <div class="tab__content p-2" v-show="active[index]"><br> {{val['text']}}</div>            
      
    </div>
  </div>
</template>

<script>
export default {
  name: "SimilarQuestions",
  props: {
    workspace_id: Number,
    widget_id: Number,

  },
  data() {
    return {
      active: [false, false, false, false, false]
    }
  },
  computed: {
    qa() {
      let qa_index = this.$store.getters.workspace(
        this.workspace_id
      ).qa_selected;
      return this.$store.getters.qa(this.workspace_id, qa_index);
    },
    country_representation() {
      return this.qa.country_representation;
    },
    getTop5_similar_questions() {
      return this.qa.top5_similar_questions;
    },
  },
  methods: {
      toggle(index) {
        this.active[index] = !this.active[index]
        this.active = [...this.active]
        console.log(index, this.active[index])
      },
  },
    
};
</script>

<style scoped>
.similar-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.container {
  cursor: default;
}
</style>