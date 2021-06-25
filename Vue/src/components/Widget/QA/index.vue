<template>
  <div>
    <textarea
      style="height: 150px"
      placeholder="Please enter your question"
      v-model="text"
    ></textarea>
    <el-button type="primary" @click="SearchData"> Answer </el-button>
    <textarea placeholder="Answer" v-model="answer"></textarea>
  </div>
</template>

<script>
export default {
  name: "QA",
  data() {
    return {
      text: "",
      answer: "",
    };
  },
  methods: {
    SearchData: function () {
      let formData = new FormData();
      formData.append("text", this.text);

      this.axios({
        url: "http://127.0.0.1:5000/func/act",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.answer = response.data["guess"];
        this.$store.state.modal.opened = true;
        this.$store.state.modal.difficulty = response.data["difficulty"];
        this.$store.state.modal.question_saved = response.data["difficulty"] === "Hard";
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

textarea {
  border: 100px;
  border-radius: 5px;
  background-color: rgba(241, 241, 241, 0.98);
  width: 800px;
  padding: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  resize: none;
}

.el-button {
  background: steelblue;
  width: 100px;
  opacity: 1;
  transition: opacity 0.3s;
}

.el-button:hover {
  opacity: 0.8;
}

.el-button:active {
  transform: scale(0.97);
}
</style>