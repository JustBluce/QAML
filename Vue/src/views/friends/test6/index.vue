<template>
  <div id="app">
    <textarea
      style="
        border: 100px;
        border-radius: 5px;
        background-color: rgba(241, 241, 241, 0.98);
        width: 800px;
        height: 150px;
        padding: 10px;
        resize: none;
      "
      placeholder="Please enter your question"
      v-model="text"
    ></textarea>
    <br />
    <el-button type="primary" @click="SearchData"> Answer </el-button>
    <br />
    <textarea
      style="
        border: 0;
        border-radius: 5px;
        background-color: rgba(241, 241, 241, 0.98);
        width: 800px;
        height: 100px;
        padding: 10px;
        resize: none;
      "
      placeholder="Answer"
      v-model="answer"
    ></textarea>
    <!--    <br>-->
    <!--    <textarea style="border:0;border-radius:5px;background-color:rgba(241,241,241,.98);width: 355px;height: 100px;padding: 10px;resize: none;" placeholder="相似句" v-model="text3"></textarea>-->
  </div>
</template>

<script>
import { VueEditor } from "vue2-editor";

export default {
  components: {
    VueEditor,
  },

  data() {
    return {
      returndata: ["", ""],
      text: "",
      answer: "",
    };
  },
  methods: {
    SearchData: function () {
      let formData = new FormData();
      formData.append("text", this.text);

      var jsons = {
        text: this.text,
      };

      this.axios({
        url: "http://127.0.0.1:5000/func/act",
        method: "POST",
        data: formData,
        // header:{
        //   'Content-Type':'application/json'  //如果写成contentType会报错
        // }
      }).then((response) => {
        this.returndata = response.data;
        this.answer = response.data["guess"];
        console.log(response);
        console.log(this.text);
        console.log(this.answer);
      });
    },
  },
};
</script>
