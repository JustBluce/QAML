<!--
Developers: Cai Zefan, Atith Gandhi, and Jason Liu
-->

<template>
  <div ref="qaContainer" class="qa-container">
    <div class="header">
      <input class="title" v-model="qa.title" />
      <a v-show="qa_count > 1" class="fas fa-trash btn" @click="deleteQA" />
    </div>
    <textarea
      class="container"
      rows="18"
      placeholder="Please enter your question"
      v-model="text"
    ></textarea>
    <el-button type="primary" @click="searchData">Submit</el-button>
    <textarea
      readonly
      class="container"
      rows="2"
      placeholder="Answer"
      v-model="answer"
    ></textarea>
    <textarea
      readonly
      class="container"
      rows="5"
      placeholder="Country representation"
      v-model="country_representation"
    ></textarea>
    <textarea
      readonly
      class="container"
      rows="5"
      placeholder="People ethnicity"
      v-model="people_ethnicity"
    ></textarea>
  </div>
</template>

<script>
import Vue from "vue";
import Modal from "./Modal";

export default {
  name: "QA",
  props: {
    workspace_id: Number,
    qa_id: Number,
  },
  components: {
    Modal,
  },
  data() {
    return {
      answer: "",
      country_representation: "",
      people_ethnicity: ""
      
    };
  },
  computed: {
    qa() {
      return this.$store.getters.qa(this.workspace_id, this.qa_id);
    },
    qa_count() {
      return this.$store.getters.workspace(this.workspace_id).qas.length;
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
      });

      this.axios({
        url: "http://127.0.0.1:5000/difficulty_classifier/classify",
        method: "POST",
        data: formData,
      }).then((response) => {
        if (response.data["difficulty"] === "Hard") {
          this.addModal("Saved !!!", "Your question is submitted.");
        } else {
          this.addModal(
            "Not saved !!!",
            "Your question has Easy level difficulty. Please try again."
          );
        }
      });

      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        if (response.data["similar_question"][0]) {
          this.addModal(
            "Warning !!! Your question is similar to the below given question. Please rewrite it again:",
            response.data["similar_question"][1]
          );
        }
      });

      this.axios({
        url: "http://127.0.0.1:5000/country_represent/country_present",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.country_representation =
          response.data["country_representation"].trim();
        this.country_representation =
          response.data["country_representation"].trim();
      });

      this.axios({
        url: "http://127.0.0.1:5000/people_info/getPeoplesInfo",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.people_ethnicity = response.data["people_ethnicity"];
        this.people_ethnicity = response.data["people_ethnicity"];
      });
    },

    addModal(header, body) {
      let ModalClass = Vue.extend(Modal);
      let modal = new ModalClass({
        propsData: { header, body },
      });
      modal.$mount();
      this.$refs.qaContainer.appendChild(modal.$el);
    },

    deleteQA() {
      this.$store.commit("deleteQA", {
        workspace_id: this.workspace_id,
        qa_id: this.qa_id,
      });
    },
  },
};
</script>

<style scoped>
.qa-container {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 500px;
  padding: 20px;
  flex-grow: 100;
}

.header {
  display: flex;
  font-size: 24px;
}

.title {
  border: 0;
  font-weight: bold;
  outline: none;
  text-overflow: ellipsis;
  padding: 0;
  flex-grow: 1;
}

.fas {
  width: 30px;
  text-align: right;
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