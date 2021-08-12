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

        <div class="backdrop" ref="backdrop">
          <div class="highlight" v-html="highlight_text">
            <!-- cloned text with <mark> tags here -->
          </div>
        </div>
        <v-textarea
          ref="textarea"
          background-color="background"
          class="highlight-textarea my-4"
          rows="10"
          label="Question"
          solo
          v-model="qa.text"
          hide-details="auto"
          @keydown="keep_looping"
        ></v-textarea>
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

        <!-- <v-card class="background mt-4 pa-2">
          <div
            v-html="qa.highlight_text"
            background-color="background"
            rows="1"
            label="Tips"
            solo
            hide-details="auto"
          ></div>
        </v-card> -->
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import { GChart } from "vue-google-charts";

export default {
  name: "QA",
  props: {
    id: Number,
  },
  components: {
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
      rules: [(value) => !!value || "Required."],
      showChart: false,
      my_var:""
    };
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.id);
    },
    qa() {
      return this.workspace.qa;
    },
    highlight() {
      return [
        { text: "🔔BUZZ", class: "yellow" },
        { text: "highlight me", class: "primary" },
      ];
    },
    highlight_text() {
      let text = this.qa.text;
      this.highlight.forEach((highlight) => {
        text = text
          .split(`${highlight.text}`)
          .join(`<mark class="${highlight.class}">${highlight.text}</mark>`);
      });
      return text.replace(/\n$/g, "\n\n");
    },
    options() {
      return {
        width: Math.max(1024, this.workspace.style.width) / 3 - 50,
        backgroundColor: "none",
      };
    },
  },

  created: function () {
    this.my_var =  setInterval(function () {
      let formData = new FormData();
      console.log(this.qa.text.lastIndexOf("🔔")>0)
      while(this.qa.text.lastIndexOf("🔔")>0)
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf("🔔")) + this.qa.text.substr(this.qa.text.lastIndexOf("🔔") + "🔔".length,this.qa.text.length)
        }
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      formData.append("date",new Date().toLocaleString('en-US',{ hour12: false, month: "2-digit", day: "2-digit",  year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }));
      formData.append("id",this.id);
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
        while(this.qa.text.lastIndexOf("🔔")>0)
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf("🔔")) + this.qa.text.substr(this.qa.text.lastIndexOf("🔔") + "🔔".length,this.qa.text.length)
        }
        this.qa.binary_search_based_buzzer = response.data["buzz"];
        this.qa.importance = response.data["importance"];
        this.highlight = response.data["buzz_word"];
        this.qa.top_guess_buzzer = response.data["top_guess"];
        if(this.qa.text.lastIndexOf(response.data["buzz_word"])>0 && response.data["flag"])
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf(response.data["buzz_word"])+10) + "🔔" + this.qa.text.substr(this.qa.text.lastIndexOf(response.data["buzz_word"])+10,this.qa.text.length)
        }
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
          if (
            this.qa.text.lastIndexOf(response.data["buzz_word"]) > 0 &&
            response.data["flag"]
          ) {
            this.qa.text =
              this.qa.text.substr(
                0,
                this.qa.text.lastIndexOf(response.data["buzz_word"]) + 10
              ) +
              "🔔" +
              this.qa.text.substr(
                this.qa.text.lastIndexOf(response.data["buzz_word"]) + 10,
                this.qa.text.length
              );
          }
          console.log(this.qa.text.lastIndexOf(response.data["buzz_word"]));
          console.log(this.qa.text.indexOf(response.data["buzz_word"]));

  methods: {
    keep_looping: _.debounce(function () {
      clearInterval(this.my_var);
      let formData = new FormData();
      console.log(new Date().toLocaleString('en-US',{ hour12: false, month: "2-digit", day: "2-digit",  year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }))
      // console.log(new Date().toString())
      while(this.qa.text.lastIndexOf("🔔")>0)
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf("🔔")) + this.qa.text.substr(this.qa.text.lastIndexOf("🔔") + "🔔".length,this.qa.text.length)
        }
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      formData.append("date",new Date().toLocaleString('en-US',{ hour12: false, month: "2-digit", day: "2-digit",  year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }));
      formData.append("id",this.id);
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
        while(this.qa.text.lastIndexOf("🔔")>0)
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf("🔔")) + this.qa.text.substr(this.qa.text.lastIndexOf("🔔") + "🔔".length,this.qa.text.length)
        }
        this.qa.binary_search_based_buzzer = response.data["buzz"];
        this.qa.importance = response.data["importance"];
        this.highlight = response.data["buzz_word"];
        this.qa.top_guess_buzzer = response.data["top_guess"];
        if(this.qa.text.lastIndexOf(response.data["buzz_word"])>0 && response.data["flag"])
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf(response.data["buzz_word"])+10) + "🔔" + this.qa.text.substr(this.qa.text.lastIndexOf(response.data["buzz_word"])+10,this.qa.text.length)
        }
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
        url: "http://127.0.0.1:5000/pronunciation/get_pronunciation",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.pronunciation = response.data["message"];
      });
    }, 1000),

    update_representation: _.debounce(function () {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      formData.append("date",new Date().toLocaleString('en-US',{ hour12: false, month: "2-digit", day: "2-digit",  year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }));
      formData.append("id",this.id);
      // this.axios({
      //   url: "http://127.0.0.1:5000/over_present/highlight",
      //   method: "POST",
      //   data: formData,
      // }).then((response) => {
      //   this.highlight_text = response.data["highlight_text"];
      //   // this.qa.importance = response.data["importance"];
      //   // this.highlight = response.data["buzz_word"];
      //   console.log(response);
      // });
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
      clearInterval(this.my_var);
      while(this.qa.text.lastIndexOf("🔔")>0)
        {
          this.qa.text= this.qa.text.substr(0,this.qa.text.lastIndexOf("🔔")) + this.qa.text.substr(this.qa.text.lastIndexOf("🔔") + "🔔".length,this.qa.text.length)
        }
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      formData.append("date",new Date().toLocaleString('en-US',{ hour12: false, month: "2-digit", day: "2-digit",  year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }));
      formData.append("id",this.id);
      this.axios({
        url: "http://127.0.0.1:5000/similar_question/retrieve_similar_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        if (response.data["similar_question"][0])
        {
              this.addResult({
                title: "Similar question detected",
                body: response.data["similar_question"][1][0]["text"],
              });
        } 
        else {
          this.axios({
            url: "http://127.0.0.1:5000/difficulty_classifier/classify",
            
            method: "POST",
            data: formData,
          }).then((response) => {
            if (response.data["difficulty"] === "Hard" || response.data["difficulty"]==="Easy")
              {
                if(response.data["difficulty"]==="Easy"):
                {
                  this.addResult({
                  title: "Easy Question",
                  body: "Your question was not difficult enough for the computer.",
                });
                }
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
                  console.log('1');
                  window.setTimeout(() => {
                    this.axios({
                      
                      url: "http://127.0.0.1:5000/func/insert",
                      method: "POST",
                      data: formData,
                    }).then((response) => {
                      console.log("HERE IS PUSH");
                      console.log("Inside this .axios");
                      // this.$router.push({ name: 'Dashboard' });
                    });
                    this.addResult({
                      title: "Saved",
                      body: "Your question is now added to the database.",
                    });
                    console.log('2');
                  }, 5000)
                 
                  
                }
              }
              else {
                this.addResult({
                  title: "Not saved",
                  body: "Your question was not difficult enough for the computer. Please try again.",
                });
              }
            // this.qa.top5_similar_questions = response.data["similar_question"];
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
      formData.append("date",new Date().toLocaleString('en-US',{ hour12: false, month: "2-digit", day: "2-digit",  year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" }));
      formData.append("id",this.id);
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
  mounted() {
    let formData = new FormData();
    formData.append("Timestamp", "2021-08-02 19:57:42");
    this.axios({
      url: "http://127.0.0.1:5000/question/Question_id",
      method: "POST",
    }).then((response) => {
      this.Question_id = response.data["Question_id"];
      console.log(response);
    });

    this.styleInterval = setInterval(
      function () {
        let backdrop = this.$refs.backdrop;
        let textarea = this.$refs.textarea;
        backdrop.style.height = textarea.$el.offsetHeight - 10 + "px";
        backdrop.style.width = textarea.$el.offsetWidth + "px";
        backdrop.scrollTop =
          document.getElementsByTagName("textarea")[0].scrollTop;
      }.bind(this),
      10
    );
  },
  beforeDestroy() {
    clearInterval(this.interval);
    clearInterval(this.styleInterval);
  },
};
</script>

<style>
.highlight-textarea textarea {
  z-index: 2;
}

.highlight {
  color: transparent;
  white-space: pre-wrap;
  word-wrap: break-word;
}

mark {
  border-radius: 3px;
  color: transparent;
}

.backdrop {
  position: absolute;
  margin-top: 10px;
  padding-left: 12px;
  padding-right: 12px;
  line-height: 1.75rem;
  z-index: 1;
  overflow: auto;
}
</style>