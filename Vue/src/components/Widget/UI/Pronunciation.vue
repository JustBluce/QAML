<!--
Developers: Damien Rene and Jason Liu
-->

<template>
  <div>
    <!-- <div class="placeholder" v-show="!qa.text">Please enter your question</div>
    <Highlighter
      :style="{ color: 'black' }"
      highlightClassName="highlight"
      :searchWords="keywords"
      :autoEscape="true"
      :textToHighlight="qa.text"
    /> -->
    <!-- <div>
      <h4> Please add the pronunciation guide for the following words </h4>
    </div> -->
    <!-- <v-textarea
      readonly    
      color="background"
      rows="1"
      placeholder="Pronunciation highlighting"
      v-model="pronunciation"
    ></v-textarea> -->
    <h4 class="mb-2" v-on:click="record">
      Please add the pronunication guide for the following words
    </h4>
    <v-data-table
      v-on:click="record"
      hide-default-header
      hide-default-footer
      dense
      :headers="headers"
      :items="pronunciation"
      class="elevation-2"
    ></v-data-table>

    <v-dialog v-model="popup" persistent max-width="500">
      <v-card>
        <v-card-title class="text-h5"> Record Pronunciation </v-card-title>
        
        <!--  <input type="file" accept="audio/*" capture id="recorder">
        <audio id="player" controls></audio> -->

        <button  @clilck="audio">Record</button>
        <button  @clilck="stop=true">stop</button>

        
       
       

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="popup = false"> Cancel </v-btn>
          <v-btn color="green darken-1" text @click="sendverification">
           Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>




<script>
import Highlighter from "vue-highlight-words";

export default {
  
  name: "Pronunciation",
  props: {
    workspace_id: Number,
  },
  components: {
    Highlighter,
  },
  data() {
    return {
      popup: false,
      //recorder: document.getElementById('recorder'),
      //player: document.getElementById('player'),
  
      stop: false,
      words: "and or the quick",
      headers: [{ text: "Word", value: "Word" }],
    };
  },
   
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },
    pronunciation() {
      return this.qa.pronunciation;
    },
    keywords() {
      return this.words.split(" ");
    },
   
  },
  methods: {
    
    paused(){
        this.pause = true
    },
      record(){
        this.popup = true; 
      },
      audio(){
        console.log("Recording Audio ")
        this.stop = false;
        const player = document.getElementById('player');

        const handleSuccess = function(stream) {
          if (window.URL) {
            player.srcObject = stream;
          } else {
            player.src = stream;
          }
        };
        while(this.stop == false){
        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(handleSuccess);
      }
    },
      
  },
};
</script>
