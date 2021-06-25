<!--
Developers: Cai Zefan and Jason Liu
-->

<template>
  <div>
    <textarea
      class="output"
      rows="6"
      placeholder="Please enter your question"
      v-model="text"
    ></textarea>
    <el-button type="primary" @click="searchData"> Answer </el-button>
    <textarea
      class="output"
      rows="1"
      placeholder="Answer"
      v-model="answer"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: "QA",
  props: {
    id: String,
  },
  data() {
    return {
      answer: "",
    };
  },
  computed: {
    text: {
      get() {
        return this.$store.getters.questions(this.id).text;
      },
      set(value) {
        this.$store.commit("updateQuestion", { id: this.id, text: value });
      },
    },
  },
  methods: {
    searchData() {
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
        this.$store.state.modal.question_saved =
          response.data["difficulty"] === "Hard";
      });
    },
  },
  created() {
    this.$store.commit("addQuestion", this.id);
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