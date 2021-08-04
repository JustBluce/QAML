<template>
  <v-container fluid class="background" style="flex-shrink: 1">
    <v-card class="mb-3">
      <v-container fluid>
        <v-card class="mb-4" color="background">
          <v-card-actions>
            <v-select
              v-model="qa.genre"
              :items="genres"
              @change="changeGenre"
              label="Question genre"
              hide-details="auto"
              dense
            ></v-select>
            <v-spacer></v-spacer>
            <v-btn icon color="primary" @click="showChart = !showChart">
              <v-icon>
                {{ showChart ? "mdi-chevron-up" : "mdi-chart-pie" }}
              </v-icon>
            </v-btn>
          </v-card-actions>
          <v-expand-transition>
            <div v-show="showChart">
              <v-divider></v-divider>
              <GChart type="PieChart" :options="options" :data="chartData" />
            </div>
          </v-expand-transition>
        </v-card>
        <v-textarea
          background-color="background"
          class="my-4"
          rows="10"
          label="Question"
          solo
          v-model="qa.text"
          hide-details="auto"
          @keydown="keep_looping"
        ></v-textarea>
        <!-- <highlightable-input
      highlight-style="background-color:yellow"
      :highlight-enabled="highlightEnabled"
          :highlight="highlight"
          class="my-4"
          rows="10"
          label="Question"
          solo
          v-model="qa.text"
          hide-details="auto"
          @keyup="keep_looping"
    /> -->
        <v-textarea
          background-color="background"
          class="my-4"
          rows="1"
          label="Answer"
          solo
          v-model="qa.answer_text"
          hide-details="auto"
          @input="update_representation"
        ></v-textarea>

        <v-btn color="primary" @click="searchData">
          Submit <v-icon>mdi-cloud-upload</v-icon>
        </v-btn>

        <div
          v-html="highlight_text"
          background-color="background"
          class="my-4"
          rows="1"
          label="Tips"
          solo
          hide-details="auto"
        ></div>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import HighlightableInput from "vue-highlightable-input";
import { GChart } from "vue-google-charts";
export default {
  name: "QA",
  props: {
    id: Number,
  },
  components: {
    HighlightableInput,
    GChart,
  },
  data() {
    return {
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
      chartData: [
        ["Subgenre", "Count"],
        ["None", 1],
      ],
      highlight_text: "There are some <font color=\"#333333\"><strong style=\"background:red\"><em>tips</em></strong></font>",
      highlight: "🔔BUZZ",
      rules: [(value) => !!value || "Required."],
      showChart: false,
      Question_id: -1,
    };
  },
  mounted: {
    Create_Question_ID() {
      formData.append("Timestamp", '2021-08-02 19:57:42');
      this.axios({
        url: "http://127.0.0.1:5000/question/Question_id",
        method: "POST",
      }).then((response) => {
        this.Question_id = response.data["Question_id"];
        console.log(response);
      });
    }
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.id);
    },
    qa() {
      return this.workspace.qa;
    },
    options() {
      return {
        width: Math.max(1024, this.workspace.style.width) / 3 - 50,
        backgroundColor: "none",
      };
    },
  },
  methods: {
    keep_looping: _.debounce(function () {
      let formData = new FormData();
      // console.log(this.qa.text.lastIndexOf("🔔BUZZ")>0)
      // while(this.qa.text.lastIndexOf("🔔BUZZ")>0)
      //   {
      //     this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf("🔔BUZZ")) + this.qa.text.substr(this.qa.text.lastIndexOf("🔔BUZZ") + "🔔BUZZ".length,this.qa.text.length)
      //   }
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      // this.qa.genre = this.selected_genre
      // if(this.answer_text === "" || this.text ==="" || this.qa.genre === "")
      //         {
      //           this.addModal(
      //           "Warning !!! Please some fields are empty","Please make sure the QA box and the Answer box are filled and the Genre is selected"
      //         );
      //         }
      // else{
      this.axios({
        url: "http://127.0.0.1:5000/func/act",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.answer = response.data["guess"];
        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/binary_search_based_buzzer/buzz_full_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.binary_search_based_buzzer = response.data["buzz"];
        this.qa.importance = response.data["importance"];
        this.highlight = response.data["buzz_word"];
        // if(this.qa.text.lastIndexOf(response.data["buzz_word"])>0 && response.data["flag"])
        // {
        //   this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf(response.data["buzz_word"])+10) + "🔔BUZZ" + this.qa.text.substr(this.qa.text.lastIndexOf(response.data["buzz_word"])+10,this.qa.text.length)
        // }
        // console.log(this.qa.text.lastIndexOf(response.data["buzz_word"]))
        // console.log(this.qa.text.indexOf(response.data["buzz_word"]))

        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        // if (response.data["similar_question"][0]) {
        //   this.addModal(
        //     "Warning !!! Your question is similar to the below given question. Please rewrite it again:",
        //     response.data["similar_question"][1][0]['text']
        //   );
        // }
        this.qa.top5_similar_questions = response.data["similar_question"];
        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/country_represent/country_present",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.country_representation =
          response.data["country_representation"];
        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/pronunciation/get_pronunciation",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.pronunciation = response.data["message"];
        console.log(response);
      });
    }, 10000),
    update_representation: _.debounce(function () {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      this.axios({
        url: "http://127.0.0.1:5000/over_present/highlight",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.highlight_text = response.data["highlight_text"];
        // this.qa.importance = response.data["importance"];
        // this.highlight = response.data["buzz_word"];
        console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/country_represent/country_present",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.country_representation =
          response.data["country_representation"];
      });
    }, 1000),
    searchData() {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
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