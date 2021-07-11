<!--
Developers: Cai Zefan and Jason Liu
-->

<template>
  <div>
    <textarea
      class="container"
      rows="5"
      placeholder="Please enter your question"
      v-model="text"
    ></textarea>
    <el-button type="primary" @click="searchData"> Answer </el-button>
    <textarea
      class="container"
      rows="1"
      placeholder="Answer"
      v-model="answer"
    ></textarea>
    <textarea
      class="container"
      rows="2"
      placeholder="Ethnicity"
      v-model="people_ethnicity"
    ></textarea>
     <textarea
      class="container"
      placeholder="Countries Represented in the question"
      v-model="country_representation"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: "QA",
  props: {
    id: Number,
  },
  data() {
    return {
      answer: "",
      people_ethnicity: "",
      gender: "",
      country_representation: "",
      difficulty: 'Easy',
      genre: ''
      
    };
  },
  computed: {
    text: {
      get() {
        return this.$store.getters.widget(this.id).text;
      },
      set(value) {
        this.$store.commit("updateWidget", { id: this.id, text: value });
      },
    },
  },
  methods: {
    searchData() {
      let formData = new FormData();
      formData.append("text", this.text);
      this.axios({
        url: "http://127.0.0.1:5000/difficulty_classifier/classify",
        method: "POST",
        data: formData,
        // header:{
        //   'Content-Type':'application/json'  //如果写成contentType会报错
        // }
      }).then((response) => {
        // this.returndata = response.data;
        this.$store.state.modal.opened = true; 
        this.difficulty = response.data["difficulty"];
        this.$store.state.modal.question_saved = response.data["difficulty"] === "Hard";
        console.log(response);
        // console.log(this.text);
        // console.log(this.answer);
      });
      this.axios({
        url: "http://127.0.0.1:5000/country_represent/country_present",
        method: "POST",
        data: formData,
        // header:{
        //   'Content-Type':'application/json'  //如果写成contentType会报错
        // }
      }).then((response) => {
        // this.returndata = response.data;
        this.country_representation = response.data["country_representation"];
        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/people_info/getPeoplesInfo",
        method: "POST",
        data: formData,
        // header:{
        //   'Content-Type':'application/json'  //如果写成contentType会报错
        // }
      }).then((response) => {
        // this.returndata = response.data;
        this.people_ethnicity = response.data["people_ethnicity"];
        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
        // header:{
        //   'Content-Type':'application/json'  //如果写成contentType会报错
        // }
      }).then((response) => {
        this.$store.state.warning_modal.opened = response.data["similar_question"][0]
        this.$store.state.warning_modal.similar_question = response.data["similar_question"][1]
        console.log(response);
      });
    },
  },
};
</script>

<style scoped>
div {
  display: flex;
  flex-direction: column;
}

.el-button {
  background: steelblue;
  width: 100px;
  margin-top: 10px;
  opacity: 1;
  transition: opacity 0.3s;
}

.el-button:hover {
  opacity: 0.8;
}

.el-button:active {
  transform: scale(0.98);
}
</style>