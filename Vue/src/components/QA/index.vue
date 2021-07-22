<!--
Developers: Cai Zefan, Atith Gandhi, and Jason Liu
-->

<template>
<<<<<<< HEAD:Vue/src/components/Workspace/QA.vue
  <div ref="qaContainer" class="qa-container">
    <div class="header">
      <input class="title" v-model="qa.title" />
      <a v-show="qa_count > 1" class="fas fa-trash btn" @click="deleteQA" />
    </div>
    <highlightable-input
=======
  <v-container fluid class="background">
    <v-card class="mb-3">
      <v-tabs v-model="qa_selected" ref="tabs" show-arrows>
        <draggable
          class="ma-0 row"
          v-model="qas"
          @update="$store.commit('updateQAs', workspace_id)"
        >
          <v-tab v-for="qa in qas" :key="qa.id" :ripple="false">{{
            qa.title
          }}</v-tab>
        </draggable>
      </v-tabs>

      <v-tabs-items v-model="qa_selected">
        <v-tab-item
          v-for="qa in qas"
          :key="qa.id"
          v-show="qa.id === qa_selected"
        >
          <v-card flat>
            <v-card-title>
              <v-text-field
                placeholder="Title"
                hide-details="auto"
                :rules="rules"
                :value="qa.title"
                @input="checkTitle"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-btn class="ml-2" elevation="4" icon @click="createQA">
                <v-icon color="open">mdi-plus</v-icon>
              </v-btn>
              <v-btn
                class="ml-2"
                elevation="4"
                icon
                :disabled="qas.length === 1"
                @click="clickDelete"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-card-title>

            <v-container fluid>
              <v-textarea
                background-color="background"
                rows="10"
                label="Question"
                solo
                v-model="qa.text"
                @input="keep_looping"
              ></v-textarea>
              <v-textarea
                background-color="background"
                rows="1"
                label="Answer"
                solo
                v-model="qa.answer_text"
                @input="update_representation"
              ></v-textarea>
              <v-btn color="primary" @click="searchData">
                Submit <v-icon>mdi-cloud-upload</v-icon>
              </v-btn>
            </v-container>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>

    <v-row no-gutters>
      <v-col>
        <v-select
          v-model="qa.genre"
          @change = "changeGenre"
          :items="genres"
          label="Question genre"
          solo
        ></v-select>
      </v-col>

      <v-col>
        <GChart type="PieChart" :options="options" :data="chartData" />
      </v-col>
    </v-row>

    <v-bottom-sheet v-model="sheet" persistent>
      <v-sheet class="text-center" height="100">
        <div class="py-3">
          Are you sure you want to delete
          <span class="font-weight-bold">{{ qa.title }}</span>
          ?
        </div>
        <v-btn text color="open" @click="deleteQA"> Yes </v-btn>
        <v-btn text color="close" @click="sheet = false"> No </v-btn>
      </v-sheet>
    </v-bottom-sheet>
  </v-container>

  <!-- <highlightable-input
>>>>>>> 3234f94b2b0d2be7374d8a7f5e4ba85149e7f878:Vue/src/components/QA/index.vue
      highlight-style="background-color:yellow"
      :highlight-enabled="highlightEnabled"
      :highlight="highlight"
      class="big-container"
      :caseSensitive=true
      placeholder="Please enter your question"
      v-model="text"
<<<<<<< HEAD:Vue/src/components/Workspace/QA.vue
    />

    <!-- <textarea
      class="container"
      rows="10"
      placeholder="Please enter your question"
      v-model="text"
      @input="keep_looping"
    ></textarea> -->
    <textarea
      class="container"
      rows="2"
      placeholder="Answer"
      v-model="answer_text"
      @input="update_representation"
    ></textarea>
    <el-button type="primary" @click="searchData">
      Submit <i class="fa fa-upload"
    /></el-button>
    <div class="two-col">
      <div class="col1">
        <div><h4>Genre</h4></div>
        <select v-model="qa.genre" @change="changeGenre">
          <option disabled value="">Select a question genre</option>
          <option v-for="(item, index) in genres" v-bind:key="index">
            {{ item }}
          </option>
        </select>
      </div>

      <div class="col2">
        <GChart type="PieChart" :options="options" :data="chartData" />
      </div>
    </div>
  </div>
=======
      @input="keep_looping"`
    /> -->
>>>>>>> 3234f94b2b0d2be7374d8a7f5e4ba85149e7f878:Vue/src/components/QA/index.vue
</template>

<script>
import draggable from "vuedraggable";
import HighlightableInput from "vue-highlightable-input";
import { GChart } from "vue-google-charts";

export default {
  name: "QA",
  props: {
    workspace_id: Number,
    qa_id: Number,
  },
  components: {
    draggable,
    HighlightableInput,
    GChart,
  },
  data() {
    return {
      highlight: [
        // { text: "chicken", style: "background-color:#f37373" },
        // { text: "noodle", style: "background-color:#fca88f" },
        // { text: "soup", style: "background-color:#bbe4cb" },
        // { text: "so", style: "background-color:#fff05e" },
        // #e91640
        // #ee4466
        // #f48aa0
        // "whatever",
        { text: "soupppppp", style: "background-color:#fff05e" },
        { text: "so", style: "border: 2px solid #73AD21;" },
      ],
      highlightEnabled: true,
      genres: [
        "Philosophy",
        "History",
        "Literature",
        "Mythology",
        "Current Events",
        "Religion",
        "Trash",
        "Social Science",
        "Science",
        "Fine Arts",
        "Geography",
      ],
      options: {
        width: 650,
        height: 400,
        backgroundColor: "none",
      },
      chartData: [
        ["Subgenre", "Count"],
        ["None", 1],
      ],
      rules: [(value) => !!value || "Required."],
      sheet: false,
    };
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.workspace_id);
    },
    qas: {
      get() {
        return this.workspace.qas;
      },
      set(value) {
        this.workspace.qas = value;
      },
    },
    qa_selected: {
      get() {
        return this.workspace.qa_selected;
      },
      set(value) {
        this.workspace.qa_selected = value;
      },
    },
    qa() {
      return this.$store.getters.qa(this.workspace_id, this.qa_selected);
    },
  },
  methods: {
<<<<<<< HEAD:Vue/src/components/Workspace/QA.vue
    // keep_looping: _.debounce(function () {
    //   let formData = new FormData();
    //   formData.append("text", this.text);
    //   formData.append("answer_text", this.answer_text);
    //   // this.qa.genre = this.selected_genre
    //   // if(this.answer_text === "" || this.text ==="" || this.qa.genre === "")
    //   //         {
    //   //           this.addModal(
    //   //           "Warning !!! Please some fields are empty","Please make sure the QA box and the Answer box are filled and the Genre is selected"
=======
    keep_looping: _.debounce(function () {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      // this.qa.genre = this.selected_genre
      // if(this.answer_text === "" || this.text ==="" || this.qa.genre === "")
      //         {
      //           this.addModal(
      //           "Warning !!! Please some fields are empty","Please make sure the QA box and the Answer box are filled and the Genre is selected"
>>>>>>> 3234f94b2b0d2be7374d8a7f5e4ba85149e7f878:Vue/src/components/QA/index.vue

    //   //         );

    //   //         }
    //   // else{
    //   this.axios({
    //     url: "http://127.0.0.1:5000/func/act",
    //     method: "POST",
    //     data: formData,
    //   }).then((response) => {
    //     this.qa.answer = response.data["guess"];
    //     console.log(response);
    //   });

    //   this.axios({
    //     url: "http://127.0.0.1:5000/binary_search_based_buzzer/buzz_full_question",
    //     method: "POST",
    //     data: formData,
    //   }).then((response) => {
    //     this.qa.binary_search_based_buzzer = response.data["buzz"];
    //     this.qa.importance = response.data["importance"];
    //     this.highlight = response.data["buzz_word"];
    //     console.log(response);
    //   });

    //   this.axios({
    //     url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
    //     method: "POST",
    //     data: formData,
    //   }).then((response) => {

        // if (response.data["similar_question"][0]) {
        //   this.addModal(
        //     "Warning !!! Your question is similar to the below given question. Please rewrite it again:",
        //     response.data["similar_question"][1][0]['text']
        //   );
        // }
    //     this.qa.top5_similar_questions = response.data["similar_question"];
    //     console.log(response);
    //   });

    //   this.axios({
    //     url: "http://127.0.0.1:5000/country_represent/country_present",
    //     method: "POST",
    //     data: formData,
    //   }).then((response) => {
    //     this.qa.country_representation =
    //       response.data["country_representation"];
    //     console.log(response);
    //   });
    //   // this.axios({
    //   //   url: "http://127.0.0.1:5000/pronunciation/get_pronunciation",
    //   //   method: "POST",
    //   //   data: formData,
    //   // }).then((response) => {
    //   //   this.qa.pronunciation = response.data["message"];
    //   //   console.log(response);
    //   // });

    // }, 1000),

    // update_representation: _.debounce(function () {
    //   let formData = new FormData();
    //   formData.append("text", this.text);
    //   formData.append("answer_text", this.answer_text);
    //   this.axios({
    //     url: "http://127.0.0.1:5000/country_represent/country_present",
    //     method: "POST",
    //     data: formData,
    //   }).then((response) => {
    //     this.qa.country_representation =
    //       response.data["country_representation"];
    //   });
    // }, 1000),

    searchData() {
      let formData = new FormData();
      formData.append("text", this.text);
      formData.append("answer_text", this.answer_text);

      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        if (response.data["similar_question"][0]) {
          this.addModal(
            "Warning !!! Your question is similar to the below given question. Please rewrite it again:",
            response.data["similar_question"][1][0]['text']
          );
        }
      });

      this.axios({
        url: "http://127.0.0.1:5000/over_present/highlight",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.highlight = response.data["highlight"];
        console.log(response);
        console.log(this.highlight);
      });
<<<<<<< HEAD:Vue/src/components/Workspace/QA.vue

=======
      this.axios({
        url: "http://127.0.0.1:5000/pronunciation/get_pronunciation",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.pronunciation = response.data["message"];
        console.log(response);
      });

      
    }, 1000),
    
    update_representation: _.debounce(function () {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
>>>>>>> 3234f94b2b0d2be7374d8a7f5e4ba85149e7f878:Vue/src/components/QA/index.vue
      this.axios({
        url: "http://127.0.0.1:5000/binary_search_based_buzzer/buzz_full_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.binary_search_based_buzzer = response.data["buzz"];
        this.qa.importance = response.data["importance"];
        console.log(response);
      });

<<<<<<< HEAD:Vue/src/components/Workspace/QA.vue
=======
    searchData() {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
>>>>>>> 3234f94b2b0d2be7374d8a7f5e4ba85149e7f878:Vue/src/components/QA/index.vue
      this.axios({
        url: "http://127.0.0.1:5000/difficulty_classifier/classify",
        method: "POST",
        data: formData,
      }).then((response) => {
        if (response.data["difficulty"] === "Hard") {
          this.axios({
            url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
            method: "POST",
            data: formData,
          }).then((response) => {
            if (response.data["similar_question"][0]) {
              this.addResult({
                title: "Similar question detected",
                body: response.data["similar_question"][1][0]["text"],
              });
            } else {
              if (
                this.qa.answer_text === "" ||
                this.qa.text === "" ||
                this.qa.genre === ""
              ) {
                this.addResult({
                  title: "Empty fields",
                  body: "Please make sure Question and Answer boxes are filled and Question Genre is selected.",
                });
              } else {
                this.axios({
                  url: "http://127.0.0.1:5000/func/insert",
                  method: "POST",
                  data: formData,
                }).then((response) => {
                  console.log(response);
                });
                this.addResult({
                  title: "Saved",
                  body: "Your question is now added to the database.",
                });
              }
            }
            // this.qa.top5_similar_questions = response.data["similar_question"];
          });
        } else {
          this.addResult({
            title: "Not saved",
            body: "Your question was not difficult enough for the computer. Please try again.",
          });
        }
      });

      // this.axios({
      //   url: "http://127.0.0.1:5000/func/country_people",
      //   method: "POST",
      //   data: formData,
      // }).then((response) => {
      //   console.log(response);
      //   this.qa.country_representation = response.data["country_representation"];
      //   this.highlight = response.data["Highlight"];
      // });
    },

    checkTitle(title) {
      if (title) {
        this.qa.title = title;
        this.$refs.tabs.onResize();
      }
    },

    createQA() {
      this.$store.commit("createQA", this.workspace_id);
    },

    clickDelete() {
      if (this.qa.text || this.qa.answer_text) {
        this.sheet = true;
      } else {
        this.deleteQA();
      }
    },

    deleteQA() {
      this.$store.commit("deleteQA", {
        workspace_id: this.workspace_id,
        qa_id: this.qa_selected,
      });
      this.sheet = false;
    },

    changeGenre() {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      this.axios({
        url: "http://127.0.0.1:5000/genre_classifier/classify",
        method: "POST",
        data: formData,
      }).then((response) => {
        console.log(response.data["subgenre"][this.qa.genre]);
        this.qa.subgenre = response.data["subgenre"][this.qa.genre];
        if (this.qa.subgenre != "") {
          let header = [["Subgenre", "Count"]];
          console.log(header.concat(this.qa.subgenre));
          this.chartData = header.concat(this.qa.subgenre);
        }
      });
    },

    addResult(result) {
      this.$store.commit("addResult", result);
    },
  },
};
</script>
<<<<<<< HEAD:Vue/src/components/Workspace/QA.vue

<style scoped>
.qa-container {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px;
  flex-grow: 1;
  min-width: 0;
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
  min-width: 0;
}

.fas {
  width: 30px;
  text-align: right;
}

.big-container {
  background-color: #f5f5f5;
  height: 200px;
  padding: 20px;
  flex-grow: 50%;
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

.highlightText {
  background: yellow;
}

.two-col {
  display: flex;
  overflow: hidden;
  overflow-x: auto;
  min-width: 0;
}

.two-col .col1,
.two-col .col2 {
  width: 30%;
}

.two-col .col1 {
  max-width: 400px;
}

.two-col .col2 {
  flex-grow: 1;
}

.two-col label {
  display: block;
}
</style>
=======
>>>>>>> 3234f94b2b0d2be7374d8a7f5e4ba85149e7f878:Vue/src/components/QA/index.vue
