<!--
Developers: Cai Zefan, Atith Gandhi, and Jason Liu
-->

<template>
  <div ref="qaContainer" class="qa-container">
    <div class="header">
      <input class="title" v-model="qa.title" />
      <a v-show="qa_count > 1" class="fas fa-trash btn" @click="deleteQA" />
    </div>
    <highlightable-input
      highlight-style="background-color:yellow"
      :highlight-enabled="highlightEnabled"
      :highlight="highlight"
      class="big-container"
      placeholder="Please enter your question"
      v-model="text"
      @input="keep_looping"
    />
    <!-- <textarea
      class="container"
      rows="15"
      placeholder="Please enter your question"
      v-model="text"
      @input="keep_looping"
    ></textarea> -->
    <textarea class="container" rows="2" placeholder="Answer"></textarea>
    <el-button type="primary" @click="searchData">
      Submit <i class="fa fa-upload"
    /></el-button>

    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>Machine Guess</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in answer" :key="user.guess">
          <td>{{ user.guess }}</td>
          <td>{{ user.score }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import HighlightableInput from "vue-highlightable-input";
import Vue from "vue";
import Modal from "@/components/Modal";

export default {
  name: "QA",
  props: {
    workspace_id: Number,
    qa_id: Number,
  },
  components: {
    Modal,
    HighlightableInput,
  },
  data() {
    return {
      answer: "",
      highlight: [
        // { text: "chicken", style: "background-color:#f37373" },
        // { text: "noodle", style: "background-color:#fca88f" },
        // { text: "soup", style: "background-color:#bbe4cb" },
        // { text: "so", style: "background-color:#fff05e" },
        // "whatever",
        { text: "soupppppp", style: "border: 2px solid #73AD21;" },
      ],
      highlightEnabled: true,
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
    keep_looping: _.debounce(function () {
      let formData = new FormData();
      formData.append("text", this.text);

      this.axios({
        url: "http://127.0.0.1:5000/func/act",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response);
        this.answer = response.data["guess"];
      });

      this.axios({
        url: "http://127.0.0.1:5000/binary_search_based_buzzer/buzz_full_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.binary_search_based_buzzer = response.data["buzz"];
        console.log(response)
        this.qa.importance = response.data["importance"];
        this.highlight = response.data['buzz_word']
      });

      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response);
        if (response.data["similar_question"][0]) {
          this.addModal(
            "Warning !!! Your question is similar to the below given question. Please rewrite it again:",
            response.data["similar_question"][1][0]["text"]
          );
        }
        this.qa.top5_similar_questions = response.data["similar_question"];
      });

      this.axios({
        url: "http://127.0.0.1:5000/country_represent/country_present",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.country_representation =
          response.data["country_representation"];
      });

      this.axios({
        url: "http://127.0.0.1:5000/func/country_people",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response);
        this.qa.country_representation =
          response.data["country_representation"];
        this.highlight = response.data["Highlight"];
      });
      this.axios({
        url: "http://127.0.0.1:5000/genre_classifier/classify",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response.data["genre"]);
        this.qa.genre = response.data["genre"];
        this.qa.subgenre = response.data["subgenre"];
      });
    }, 2000),

    searchData() {
      let formData = new FormData();
      formData.append("text", this.text);
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
        url: "http://127.0.0.1:5000/genre_classifier/classify",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response.data["genre"]);
      });
      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        if (response.data["similar_question"][0]) {
          this.addModal(
            "Warning !!! Your question is similar to the below given question. Please rewrite it again:",
            response.data["similar_question"][1][0]["text"]
          );
        }
        this.qa.top5_similar_questions = response.data["similar_question"];
      });

      this.axios({
        url: "http://127.0.0.1:5000/func/country_people",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response);
        this.qa.country_representation =
          response.data["country_representation"];
        this.highlight = response.data["Highlight"];
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
.big-container {
  background-color: #f5f5f5;
  height: 200px;
  padding: 20px;
  flex-grow: 50%;
}

.qa-container {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px;
  flex-grow: 1;
  border-left: 2px solid steelblue;
  border-right: 2px solid steelblue;
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
  margin-bottom: 20px;
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