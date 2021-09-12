<!--
Developers: Jason Liu, Raj Shah, Atith Gandhi, Damian Rene, and Cai Zefan
-->

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
            <v-btn
              id="toggleChart"
              icon
              color="primary"
              @click="showChart = !showChart"
            >
              <v-icon>
                {{ showChart ? "mdi-chevron-up" : "mdi-chart-pie" }}
              </v-icon>
              <v-tooltip bottom activator="#toggleChart">
                <span v-if="showChart">Close genre chart</span>
                <span v-else>Show genre chart</span>
              </v-tooltip>
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
          <div class="highlight" v-html="highlight_text"></div>
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

        <v-row class="mx-1" no-gutters>
          <v-btn color="primary" @click="searchData">
            Submit <v-icon right>mdi-cloud-upload</v-icon>
          </v-btn>

          <v-spacer></v-spacer>

          <vue-blob-json-csv
            @error="handleError"
            file-type="json"
            :file-name="this.workspace.title"
            :data="[
              {
                Question: this.qa.text,
                Answer: this.qa.answer_text,
                Genre: this.qa.genre,
              },
            ]"
            class="button is-primary"
            color="primary"
          >
            <v-btn color="primary">
              Download <v-icon right>mdi-cloud-download</v-icon>
            </v-btn>
          </vue-blob-json-csv>
        </v-row>
      </v-container>
    </v-card>

    <v-dialog v-model="popup" persistent max-width="500">
      <v-card>
        <v-card-title class="text-h5"> Verify email address </v-card-title>
        <v-card-text
          >To ensure the security of our service we ask that you verify your
          email address. An email should have been sent to you when you created
          your account. If you do not have this email, please click the resend
          email address button to try again.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="popup = false"> Cancel </v-btn>
          <v-btn color="green darken-1" text @click="sendverification">
            Resend Email
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>


<script>
import { GChart } from "vue-google-charts";
import firebase from "firebase";

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
      popup: false,
      email: "",
      user: null,
      password: "",
      showPassword: false,
      emailRules: [
        (v) => !!v || "E-mail is required",
        //(v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],
      passwordRules: [
        (v) => !!v || "Password is required",
        // (v) => v.length >= 8 || "Min 8 characters",
      ],
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
      Question_id: -1,
      points: 0,
      textarea: {},
      interval: null,
      highlightInterval: null,
      qid: "",
      user_id: "",
    };
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.id);
    },
    qa() {
      return this.workspace.qa;
    },
    widget_types() {
      return this.workspace.widgets.map((widget) => widget.type);
    },
    highlight() {
      return this.qa.highlight_words;
    },
    highlight_text() {
      let highlight_regex = new RegExp(
        Object.keys(this.highlight).join("|"),
        "gi"
      );
      return this.qa.text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n$/g, "\n\n")
        .replace(
          highlight_regex,
          (word) => `<mark class="${this.highlight[word]}">${word}</mark>`
        );
    },
    genreChartData() {
      return this.$store.state.genreChartData;
    },
    options() {
      return {
        width: Math.max(1024, this.workspace.style.width) / 3 - 50,
        backgroundColor: "none",
      };
    },
  },

  created: function () {
    this.user_id = firebase.auth().currentUser.uid;
    // console.log(this.user_id)
    this.interval = setInterval(
      function () {
        this.qid =
          this.user_id +
          new Date().toLocaleString("en-US", {
            hour12: false,
            month: "2-digit",
            day: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          });
        this.qa.highlight_words = {};

        this.updateGuess();
        this.updateBuzzer();
        this.updateSimilarity();
        this.updateCountry();
        this.updatePronunciation();
      }.bind(this),
      15000
    );
  },

  methods: {
    sendverification() {
      this.popup = false;
      alert(
        "Verification email sent! Please check the email connected to this account."
      );
      const currentUser = this.user;
      firebase
        .auth()
        .currentUser.sendEmailVerification()
        .then(() => {
          // console.log("Sent Verification to: " + currentUser.email);
          // Email verification sent!
          // ...
        });
    },

    handleError() {
      alert("Error in downloading the JSON File. Try it after some time !!!");
    },

    keep_looping: _.debounce(function () {
      // this.highlight_words = {}
      console.log(this.qa.highlight_words);
      clearInterval(this.interval);

      this.updateGuess();
      this.updateBuzzer();
      this.updateSimilarity();
      this.updateCountry();
      this.updatePronunciation();
    }, 1000),

    update_representation: _.debounce(function () {
      this.updateCountry();
    }, 1000),

    searchData() {
      this.user = firebase.auth().currentUser;
      if (this.user.emailVerified) {
        let formData = new FormData();
        formData.append("text", this.qa.text);
        formData.append("answer_text", this.qa.answer_text);
        formData.append(
          "date",
          new Date().toLocaleString("en-US", {
            hour12: false,
            month: "2-digit",
            day: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          })
        );
        formData.append("user_id", this.user_id);
        formData.append("qid", this.qid);
        formData.append("genre", this.qa.genre);

        this.axios({
          url: "http://127.0.0.1:5000/genre_classifier/genre_data",
          method: "POST",
          data: formData,
        }).then((response) => {
          let genre_data = response.data["genre_data"];
          this.questions_list = response.data["questions_list"];
          console.log(genre_data);
          if (genre_data.length != 0) {
            let header = [["Genre", "Count"]];
            for (let i = 0; i < genre_data.length; i++) {
              header.push(genre_data[i]);
            }
            // console.log(header.concat(this.qa.subgenre));
            this.genreChartData = header;
            console.log(this.genreChartData);
          }
          console.log(this.highlight_words);
        });
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
            this.axios({
              url: "http://127.0.0.1:5000/difficulty_classifier/classify",
              method: "POST",
              data: formData,
            }).then((response) => {
              if (
                response.data["difficulty"] === "Hard" ||
                response.data["difficulty"] === "Easy"
              ) {
                if (response.data["difficulty"] === "Easy") {
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
                  // console.log("1");
                  window.setTimeout(() => {
                    this.axios({
                      url: "http://127.0.0.1:5000/func/insert",
                      method: "POST",
                      data: formData,
                    }).then((response) => {
                      // console.log("HERE IS PUSH");
                      this.points = response.data["points"];
                      console.log(this.points);
                      // this.$router.push({ name: 'Dashboard' });
                      this.addResult({
                        title: "Saved",
                        body:
                          "Your question is now added to the database. Number of points are:" +
                          this.points,
                      });
                    });

                    // console.log("2");
                  }, 5000);
                }
              } else {
                this.addResult({
                  title: "Not saved",
                  body: "Your question was not difficult enough for the humans. Please try again.",
                });
              }
              // this.qa.top5_similar_questions = response.data["similar_question"];
            });
          }
        });
      } else {
        this.popup = true;
      }
    },

    changeGenre() {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append(
        "date",
        new Date().toLocaleString("en-US", {
          hour12: false,
          month: "2-digit",
          day: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
      formData.append("id", this.user_id);
      formData.append("qid", this.qid);
      formData.append("user_id", this.user_id);
      this.axios({
        url: "http://127.0.0.1:5000/genre_classifier/classify",
        method: "POST",
        data: formData,
      }).then((response) => {
        // console.log(response.data["subgenre"][this.qa.genre]);
        this.qa.subgenre = response.data["subgenre"][this.qa.genre];
        if (this.qa.subgenre != "") {
          let header = [["Subgenre", "Count"]];
          // console.log(header.concat(this.qa.subgenre));
          this.chartData = header.concat(this.qa.subgenre);
        }
      });
    },

    updateGuess() {
      this.updateQA("func/act");
    },

    updateBuzzer() {
      if (!this.widget_types.includes("Buzzer")) {
        return;
      }
      this.updateQA(
        "binary_search_based_buzzer/buzz_full_question",
        function (res) {
          if (
            this.qa.text.lastIndexOf(res.data["buzz_word"]) > 0 &&
            res.data["flag"]
          ) {
            if (this.qa.buzz_word_this in this.qa.highlight_words) {
              delete this.qa.highlight_words[this.qa.buzz_word_this];
            }
            this.qa.buzz_word_this = res.data["buzzer_last_word"];
            for (let i = 0; i < res.data["remove_highlight"].length; i++) {
              delete this.qa.highlight_words[res.data["remove_highlight"][i]];
            }
            for (let i = 0; i < res.data["hightlight_words"].length; i++) {
              this.qa.highlight_words[res.data["hightlight_words"][i]] =
                "Buzzer";
            }
            this.qa.highlight_words[res.data["buzzer_last_word"]] = "yellow";
          } else {
            if (this.qa.buzz_word_this in this.qa.highlight_words) {
              delete this.qa.highlight_words[this.qa.buzz_word_this];
            }
          }
        }
      );
    },

    updateSimilarity() {
      if (!this.widget_types.includes("SimilarQuestions")) {
        return;
      }
      this.updateQA("similar_question/retrieve_similar_question");
    },

    updateCountry() {
      if (!this.widget_types.includes("CountryRepresentation")) {
        return;
      }
      this.updateQA("country_represent/country_present", function (res) {
        for (let i = 0; i < res.data["current_over_countries"].length; i++) {
          this.qa.highlight_words[res.data["current_over_countries"][i]] =
            "CountryRepresentation";
        }
      });
    },

    updatePronunciation() {
      if (!this.widget_types.includes("Pronunciation")) {
        return;
      }
      this.updateQA("pronunciation/get_pronunciation", function (res) {
        for (let i = 0; i < res.data["list_of_words_to_remove"].length; i++) {
          delete this.qa.highlight_words[
            res.data["list_of_words_to_remove"][i]
          ];
        }
        for (let i = 0; i < res.data["message"].length; i++) {
          this.qa.highlight_words[res.data["message"][i]["Word"]] =
            "Pronunciation";
        }
      });
    },

    updateQA(method, more = function () {}) {
      const backendFrontendMap = {
        // backend response key: frontend qa key
        guess: "answer",
        buzz: "binary_search_based_buzzer",
        top_guess: "top_guess_buzzer",
        similar_question: "top5_similar_questions",
        country_representation: "country_representation",
        message: "message",
      };

      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      formData.append(
        "date",
        new Date().toLocaleString("en-US", {
          hour12: false,
          month: "2-digit",
          day: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
      formData.append("user_id", this.user_id);
      formData.append("qid", this.qid);

      this.axios({
        url: `http://127.0.0.1:5000/${method}`,
        method: "POST",
        data: formData,
      }).then((res) => {
        backendFrontendMap.forEach((key) => {
          if (res.data[key]) {
            this.qa[backendFrontendMap[key]] = res.data[key];
          }
        });
        more(res);
      });
    },

    addResult(result) {
      this.$store.commit("addResult", {
        workspace_id: this.id,
        result: result,
      });
    },

    after_click_submit_button() {
      const user = firebase.auth().currentUser;
      let formData = new FormData();
      formData.append("username", user.displayName);
      formData.append("email", user.email);
      formData.append("UID", user.uid);
      this.axios({
        url: "http://127.0.0.1:5000/test1/json",
        method: "POST",
      }).then((response) => {
        this.Question_id = response.data["Question_id"];
        console.log(response);
      });
    },
  },

  mounted() {
    this.user = firebase.auth().currentUser;
    if (this.user.emailVerified) {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.qa.answer_text);
      formData.append(
        "date",
        new Date().toLocaleString("en-US", {
          hour12: false,
          month: "2-digit",
          day: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
      formData.append("user_id", this.user_id);
      formData.append("qid", this.qid);
      formData.append("genre", this.qa.genre);
      if (this.user_id != "") {
        this.axios({
          url: "http://127.0.0.1:5000/genre_classifier/genre_data",
          method: "POST",
          data: formData,
        }).then((response) => {
          let genre_data = response.data["genre_data"];
          this.questions_list = response.data["questions_list"];
          console.log(genre_data);
          this.showGenreChart = true;
          if (genre_data.length != 0) {
            let header = [["Genre", "Count"]];
            for (let i = 0; i < genre_data.length; i++) {
              header.push(genre_data[i]);
            }
            // console.log(header.concat(this.qa.subgenre));
            this.genreChartData = header;
            console.log(this.genreChartData);
          }
          console.log(this.highlight_words);
        });
      }
    }
    firebase.auth().onAuthStateChanged((user) => {
      if (user.email) {
        this.user = user;
      }
    });

    this.highlightInterval = setInterval(
      function () {
        let backdrop = this.$refs.backdrop;
        let textarea = this.$refs.textarea;
        backdrop.style.height = textarea.$el.offsetHeight - 10 + "px";
        backdrop.style.width = textarea.$el.offsetWidth + "px";
        backdrop.scrollTop =
          textarea.$el.getElementsByTagName("textarea")[0].scrollTop;
      }.bind(this),
      10
    );
  },

  beforeDestroy() {
    clearInterval(this.interval);
    clearInterval(this.highlightInterval);
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
  /* display: inline-block; */
  /* border-radius: 5px; */
  color: transparent;
  opacity: 0.8;
}

.backdrop {
  position: absolute;
  margin-top: 10px;
  padding-left: 13px;
  padding-right: 12px;
  line-height: 1.75rem;
  z-index: 1;
  overflow: auto;
}
</style>
