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

        <div style="position: relative">
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

          <v-fab-transition>
            <v-btn
              id="answerWiki"
              v-if="wikiShow"
              :href="wiki.link"
              target="_blank"
              color="primary"
              class="mt-2"
              absolute
              x-small
              right
              fab
            >
              <v-icon>mdi-wikipedia</v-icon>
              <v-menu
                open-on-hover
                bottom
                offset-y
                max-width="400"
                activator="#answerWiki"
              >
                <v-card>
                  <v-list-item three-line>
                    <v-list-item-content>
                      <v-list-item-title>{{ wiki.title }}</v-list-item-title>
                      <v-list-item-subtitle>{{
                        wiki.extract
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <img :src="wiki.image" height="80" class="py-2" />
                  </v-list-item>
                </v-card>
              </v-menu>
            </v-btn>
          </v-fab-transition>

          <v-textarea
            background-color="background"
            class="my-4"
            rows="1"
            label="Answer"
            solo
            v-model="qa.answer_text"
            hide-details="auto"
            @input="update_representation"
            @change="linkWikipedia()"
          ></v-textarea>
        </div>

        <v-row class="mx-1" no-gutters>
          <v-btn color="primary" @click="searchData">
            Submit <v-icon right>mdi-cloud-upload</v-icon>
          </v-btn>

          <v-spacer></v-spacer>

          <v-btn color="primary" @click="downloadQuestion()">
            Download <v-icon right>mdi-cloud-download</v-icon>
          </v-btn>
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
import fileDownload from "js-file-download";
import jsonFormat from "json-format";
import wiki from "wikijs";

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
      wikiShow: false,
      wiki: {
        title: "",
        link: "",
        image: "",
        extract: "",
      },
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
    answer_wiki() {
      return this.wiki.title || this.qa.answer_text;
    },
    highlight_text() {
      let highlights = Object.fromEntries(
        Object.entries(this.qa.highlight_words).map(([k, v]) => [
          this.uniform(k),
          v,
        ])
      );
      let highlight_regex = new RegExp(Object.keys(highlights).join("|"), "gi");
      return this.qa.text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n$/g, "\n\n")
        .replace(
          highlight_regex,
          (word) =>
            `<mark class="${highlights[this.uniform(word)]}">${word}</mark>`
        );
    },
    genreChartData: {
      get() {
        return this.$store.state.genreChartData;
      },
      set(value) {
        this.$store.state.genreChartData = value;
      },
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
    this.qid =
      this.user_id +
      " " +
      new Date().toLocaleString("en-US", {
        hour12: false,
        month: "2-digit",
        day: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    // console.log(this.user_id)
    this.interval = setInterval(
      function () {
        this.qa.highlight_words = {};
        let formData = new FormData();

        // console.log(this.qa.text.lastIndexOf("🔔") > 0);
        // while (this.qa.text.lastIndexOf("🔔") > 0) {
        //   this.qa.text =
        //     this.qa.text.substr(0, this.qa.text.lastIndexOf("🔔")) +
        //     this.qa.text.substr(
        //       this.qa.text.lastIndexOf("🔔") + "🔔".length,
        //       this.qa.text.length
        //     );
        // }
        formData.append("text", this.qa.text);
        formData.append("answer_text", this.answer_wiki);
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
          // console.log(response);
        });
        this.axios({
          url: "http://127.0.0.1:5000/binary_search_based_buzzer/buzz_full_question",
          method: "POST",
          data: formData,
        }).then((response) => {
          // while (this.qa.text.lastIndexOf("🔔") > 0) {
          //   this.qa.text =
          //     this.qa.text.substr(0, this.qa.text.lastIndexOf("🔔")) +
          //     this.qa.text.substr(
          //       this.qa.text.lastIndexOf("🔔") + "🔔".length,
          //       this.qa.text.length
          //     );
          // }

          this.qa.binary_search_based_buzzer = response.data["buzz"];
          this.qa.importance = response.data["importance"];
          // this.highlight = response.data["buzz_word"];
          this.qa.top_guess_buzzer = response.data["top_guess"];
          if (
            this.qa.text.lastIndexOf(response.data["buzz_word"]) > 0 &&
            response.data["flag"]
          ) {
            if (this.qa.buzz_word_this in this.qa.highlight_words) {
              delete this.qa.highlight_words[this.qa.buzz_word_this];
            }
            this.qa.buzz_word_this = response.data["buzzer_last_word"];

            for (let i = 0; i < response.data["remove_highlight"].length; i++) {
              delete this.qa.highlight_words[
                response.data["remove_highlight"][i]
              ];
            }
            this.qa.highlight_words[response.data["buzzer_last_word"]] =
              "yellow";
            for (let i = 0; i < response.data["highlight_words"].length; i++) {
              this.qa.highlight_words[response.data["highlight_words"][i]] =
                "Buzzer";
            }

            // this.qa.text =
            //   this.qa.text.substr(
            //     0,
            //     this.qa.text.lastIndexOf(response.data["buzz_word"]) + 10
            //   ) +
            //   "🔔" +
            //   this.qa.text.substr(
            //     this.qa.text.lastIndexOf(response.data["buzz_word"]) + 10,
            //     this.qa.text.length
            //   );
          } else {
            if (this.qa.buzz_word_this in this.qa.highlight_words) {
              delete this.qa.highlight_words[this.qa.buzz_word_this];
            }
          }
          // console.log(this.qa.text.lastIndexOf(response.data["buzz_word"]));
          // console.log(this.qa.text.indexOf(response.data["buzz_word"]));
          // console.log(response);
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
          // console.log(response);
        });
        this.axios({
          url: "http://127.0.0.1:5000/country_represent/country_present",
          method: "POST",
          data: formData,
        }).then((response) => {
          this.qa.country_representation =
            response.data["country_representation"];
          for (
            let i = 0;
            i < response.data["current_over_countries"].length;
            i++
          ) {
            this.qa.highlight_words[
              response.data["current_over_countries"][i]
            ] = "CountryRepresentation";
          }
          // console.log(this.highlight_words)
          // console.log(response);
        });
        this.axios({
          url: "http://127.0.0.1:5000/entity_represent/entity_present",
          method: "POST",
          data: formData,
        }).then((response) => {
          this.qa.entity_representation =
            response.data["entity_representation"];
          for (
            let i = 0;
            i < response.data["current_over_entities"].length;
            i++
          ) {
            this.qa.highlight_words[
              response.data["current_over_entities"][i]
            ] = "purple";
          }
          // console.log(this.highlight_words)
          // console.log(response);
        });
        this.axios({
          url: "http://127.0.0.1:5000/pronunciation/get_pronunciation",
          method: "POST",
          data: formData,
        }).then((response) => {
          this.qa.pronunciation = response.data["message"];
          // console.log( response.data["list_of_words_to_remove"]);
          for (
            let i = 0;
            i < response.data["list_of_words_to_remove"].length;
            i++
          ) {
            delete this.qa.highlight_words[
              response.data["list_of_words_to_remove"][i]
            ];
          }
          for (let i = 0; i < response.data["message"].length; i++) {
            this.qa.highlight_words[response.data["message"][i]["Word"]] =
              "Pronunciation";
          }
          // console.log(this.highlight_words)
          // console.log(response);
        });
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
    keep_looping: _.debounce(function () {
      // this.highlight_words = {}
      clearInterval(this.interval);
      console.log(this.answer_wiki);

      let formData = new FormData();
      // console.log(
      //   new Date().toLocaleString("en-US", {
      //     hour12: false,
      //     month: "2-digit",
      //     day: "2-digit",
      //     year: "numeric",
      //     hour: "2-digit",
      //     minute: "2-digit",
      //     second: "2-digit",
      //   })
      // );
      // console.log(new Date().toString())
      // while (this.qa.text.lastIndexOf("🔔") > 0) {
      //   this.qa.text =
      //     this.qa.text.substr(0, this.qa.text.lastIndexOf("🔔")) +
      //     this.qa.text.substr(
      //       this.qa.text.lastIndexOf("🔔") + "🔔".length,
      //       this.qa.text.length
      //     );
      // }
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.answer_wiki);
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
        url: "http://127.0.0.1:5000/func/act",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.answer = response.data["guess"];
        // console.log(response);
      });
      this.axios({
        url: "http://127.0.0.1:5000/binary_search_based_buzzer/buzz_full_question",
        method: "POST",
        data: formData,
      }).then((response) => {
        // while (this.qa.text.lastIndexOf("🔔") > 0) {
        //   this.qa.text =
        //     this.qa.text.substr(0, this.qa.text.lastIndexOf("🔔")) +
        //     this.qa.text.substr(
        //       this.qa.text.lastIndexOf("🔔") + "🔔".length,
        //       this.qa.text.length
        //     );
        // }

        this.qa.binary_search_based_buzzer = response.data["buzz"];
        this.qa.importance = response.data["importance"];
        // this.highlight = response.data["buzz_word"];

        this.qa.top_guess_buzzer = response.data["top_guess"];
        if (
          this.qa.text.lastIndexOf(response.data["buzz_word"]) > 0 &&
          response.data["flag"]
        ) {
          if (this.qa.buzz_word_this in this.qa.highlight_words) {
            delete this.qa.highlight_words[this.qa.buzz_word_this];
          }
          this.qa.buzz_word_this = response.data["buzzer_last_word"];
          //
          for (let i = 0; i < response.data["remove_highlight"].length; i++) {
            delete this.qa.highlight_words[
              response.data["remove_highlight"][i]
            ];
          }
          for (let i = 0; i < response.data["highlight_words"].length; i++) {
            this.qa.highlight_words[response.data["highlight_words"][i]] =
              "Buzzer";
          }
          this.qa.highlight_words[response.data["buzzer_last_word"]] = "yellow";
          // this.qa.text =
          //   this.qa.text.substr(
          //     0,
          //     this.qa.text.lastIndexOf(response.data["buzz_word"]) + 10
          //   ) +
          //   "🔔" +
          //   this.qa.text.substr(
          //     this.qa.text.lastIndexOf(response.data["buzz_word"]) + 10,
          //     this.qa.text.length
          //   );
        } else {
          if (this.qa.buzz_word_this in this.qa.highlight_words) {
            delete this.qa.highlight_words[this.qa.buzz_word_this];
          }
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
        for (
          let i = 0;
          i < response.data["current_over_countries"].length;
          i++
        ) {
          this.qa.highlight_words[response.data["current_over_countries"][i]] =
            "CountryRepresentation";
        }
      });
      this.axios({
        url: "http://127.0.0.1:5000/entity_represent/entity_present",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.entity_representation =
          response.data["entity_representation"];
        for (
          let i = 0;
          i < response.data["current_over_entities"].length;
          i++
        ) {
          this.qa.highlight_words[response.data["current_over_entities"][i]] =
            "EntityRepresentation";
        }
        // console.log(this.highlight_words)
      });
      this.axios({
        url: "http://127.0.0.1:5000/pronunciation/get_pronunciation",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.pronunciation = response.data["message"];
        for (
          let i = 0;
          i < response.data["list_of_words_to_remove"].length;
          i++
        ) {
          delete this.qa.highlight_words[
            response.data["list_of_words_to_remove"][i]
          ];
        }
        // console.log("_________________");
        // console.log(response.data["list_of_words_to_remove"]);
        // console.log("_________________");
        for (let i = 0; i < response.data["message"].length; i++) {
          this.qa.highlight_words[response.data["message"][i]["Word"]] =
            "Pronunciation";
        }
      });
    }, 1000),
    update_representation: _.debounce(function () {
      let formData = new FormData();
      formData.append("text", this.qa.text);
      formData.append("answer_text", this.answer_wiki);
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
        for (
          let i = 0;
          i < response.data["current_over_countries"].length;
          i++
        ) {
          this.qa.highlight_words[response.data["current_over_countries"][i]] =
            "CountryRepresentation";
        }
        // console.log(this.highlight_words)
      });

      this.axios({
        url: "http://127.0.0.1:5000/entity_represent/entity_present",
        method: "POST",
        data: formData,
      }).then((response) => {
        this.qa.entity_representation =
          response.data["entity_representation"];
        for (
          let i = 0;
          i < response.data["current_over_entities"].length;
          i++
        ) {
          this.qa.highlight_words[response.data["current_over_entities"][i]] =
            "EntityRepresentation";
        }
        // console.log(this.highlight_words)
      });

    }, 1000),
    searchData() {
      //clearInterval(this.interval);
      // while (this.qa.text.lastIndexOf("🔔") > 0) {
      //   this.qa.text =
      //     this.qa.text.substr(0, this.qa.text.lastIndexOf("🔔")) +
      //     this.qa.text.substr(
      //       this.qa.text.lastIndexOf("🔔") + "🔔".length,
      //       this.qa.text.length
      //     );
      // }
      this.user = firebase.auth().currentUser;
      if (this.user.emailVerified) {
        let formData = new FormData();
        formData.append("text", this.qa.text);
        formData.append("answer_text", this.answer_wiki);
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
          //console.log(genre_data);
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
      formData.append("UID", user.uid);-p
      this.axios({
        url: "http://127.0.0.1:5000/test1/json",
        method: "POST",
      }).then((response) => {
        this.Question_id = response.data["Question_id"];
        console.log(response);
      });
    },
    downloadQuestion() {
      fileDownload(
        jsonFormat({
          Question: this.qa.text,
          Answer: this.qa.answer_text,
          Genre: this.qa.genre,
        }),
        `${this.workspace.title}.json`
      );
    },
    linkWikipedia() {
      wiki()
        .page(this.qa.answer_text)
        .then((page) => {
          this.wikiShow = true;
          this.wiki.link = page.url();
          return page.chain().image().summary().request();
        })
        .then((data) => {
          this.wiki.title = data.title;
          this.wiki.image = data.image.name ? data.image.thumbnail.source : "";
          let extract = data.extract;
          while (extract != (extract = extract.replace(/\([^\(\)]*\)/g, " "))); // Remove nested parens
          this.wiki.extract = extract;
        })
        .catch((e) => {
          this.wikiShow = false;
          this.wiki.title = "";
        });
    },
    uniform(str) {
      return str.toUpperCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    },
  },
  mounted() {
    let formData = new FormData();
    // formData.append("Timestamp", "2021-08-02 19:57:42");
    // this.axios({
    //   url: "http://127.0.0.1:5000/question/Question_id",
    //   method: "POST",
    // }).then((response) => {
    //   this.Question_id = response.data["Question_id"];
    //   console.log(response);
    // });
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

    this.linkWikipedia();
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
  padding-left: 12px;
  padding-right: 12px;
  line-height: 1.75rem;
  z-index: 1;
  overflow: auto;
}
</style>
