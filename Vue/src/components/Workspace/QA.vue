<!--
Developers: Cai Zefan and Jason Liu
-->

<template>
  <div class="qa-container">
    <input class="title" v-model="qa.title" />
    <textarea
      class="container"
      rows="18"
      placeholder="Please enter your question"
      v-model="text"
    ></textarea>
    <el-button type="primary" @click="searchData">Submit</el-button>
    <textarea
      class="container"
      rows="2"
      placeholder="Answer"
      v-model="answer"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: "QA",
  props: {
    workspace_id: Number,
    qa_id: Number,
  },
  data() {
    return {
      answer: "",
    };
  },
  computed: {
    qa() {
      return this.$store.getters.qa(this.workspace_id, this.qa_id);
    },
    text: {
      get() {
        return this.qa.text;
      },
      set(value) {
        this.$store.commit("updateQA", {
          workspace_id: this.workspace_id,
          payload: { id: this.qa_id, text: value },
        });
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
        if (response.data["difficulty"] === "Hard") {
          this.$store.commit("modalText", {
            header: "Saved !!!",
            body: "Your question is submitted.",
          });
        } else {
          this.$store.commit("modalText", {
            header: "Not saved !!!",
            body: "Your question has Easy level difficulty. Please try again.",
          });
        }
      });
    },
  },
};
</script>

<style scoped>
.qa-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  padding: 20px;
  flex-grow: 100;
}

.title {
  border: 0;
  font-weight: bold;
  font-size: 24px;
  outline: none;
  text-overflow: ellipsis;
  padding: 0;
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