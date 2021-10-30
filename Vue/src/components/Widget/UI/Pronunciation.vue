<!--
Developers: Damian Rene and Jason Liu
-->

<template>
  <div>
   
    <h4 class="mb-2" @click="showpopup">
      Please add the pronunication guide for the following words
    </h4>
    
    <v-data-table
      
      hide-default-header
      hide-default-footer
      dense
      :headers="headers"
      :items="pronunciation"
      class="elevation-2"
      @click:row="showpopup"
      
    ></v-data-table>
  
  <div style="margin-top: 10%;"></div>

    

    <v-dialog v-model="popup" persistent max-width="700">
      <v-card>
        <v-card-title class="text-h5"> Record Pronunciation </v-card-title>
        <div class="form-group" :class="{ 'form-group--error': $v.word.$error }">
          
         <v-text-field
            v-model="word"
            
            text-algin="center"
            style="margin-left:20%; margin-right:20%; margin-top:2%;"
            label="Word You are Recording"
            filled
          ></v-text-field>
          
          </div>
       

        <v-row align="center" justify="center">
          
           <av-waveform 
           id="waveform"
           :audio-controls="false"
           :canv-width="100"
            v-bind:audio-src="this.audioURL"
          ></av-waveform>

          <v-btn
          :disabled="this.word.length == 0"
           v-bind:class="{ pulse: recording, 'mx-2': hasError }"
          @click="record"
          class="mx-2"
          fab
          large
          v-bind:color="recording ? 'red' : 'accent'"
        >
          <v-icon dark>
            mdi-microphone
          </v-icon>
        </v-btn>
        
       

        <v-btn
          id="stop"
          :disabled="this.word.length == 0"
         
          class="mx-2"
          fab
          large
          color="accent"
        >
          <v-icon dark>
            mdi-square
          </v-icon>
        </v-btn>

        <div style="font-size:210%; color: red;margin-left:2%;margin-right:2%;"> {{ timerCount }}</div>
    
        

       <audio id="player" controls></audio>
          
          
        </v-row>
            
        
      

       
        
      


        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="popup=false">
           Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>




<script>
import Highlighter from "vue-highlight-words";
import firebase from "firebase";
import Vuelidate from 'vuelidate'
import { required, minLength, between } from 'vuelidate/lib/validators'


const player = document.getElementById('player');
const downloadLink = document.getElementById('download');





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
      timerEnabled: false,
      timerCount: 5.00,
      hasError: false,
      audioURL: "",
      popup: false,
      select: false, 
      word: "",
      recording: false,
      words: "and or the quick",
      headers: [{ text: "Word", value: "Word" }],
    };
  },
   watch: {

            timerEnabled(value) {
                if (value) {
                    setTimeout(() => {
                        this.timerCount--;
                    }, 1000);
                }
            },

            timerCount: {
                handler(value) {

                    if (value > 0 && this.timerEnabled) {
                        setTimeout(() => {
                            this.timerCount--;
                        }, 1000);
                    }

                },
                immediate: true // This ensures the watcher is triggered upon creation
            }
       },
  
  validations: {
    word: {
      required,
      minLength: minLength(4)
    }
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
   
      
      showpopup (item, row) {   
      this.popup = true;    
     
      console.log(item.name)
      //item.name - selected id
    },
      
      
      record(){
        this.recording = true
        this.timerEnabled = true
       
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const mediaRecorder = new MediaRecorder(stream);
          const stopButton = document.getElementById('stop');
          const player = document.getElementById('player');
          const waveform = document.getElementById('waveform');
          
          mediaRecorder.start();

          const audioChunks = [];
          mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
          });

          mediaRecorder.addEventListener("stop", () => {
            
             const audioBlob = new Blob(audioChunks, { 'type' : 'audio/mpeg-3' });
            const audioUrl = URL.createObjectURL(audioBlob);
            this.audioURL = audioUrl;
            player.src = audioUrl;
            


            const title = this.word + ".wav"
            const file = new File([audioBlob], title);
            let formData = new FormData();
            formData.append('file' ,file, title);
            //formData.append('title', title);
            

             this.axios({
            url: "http://127.0.0.1:5000/pronunciation/send_files",
            method: "POST",
            headers: {
          "content-type": "multipart/form-data",
            },
            data: formData,})
             .then((response) =>{
               console.log(response)
             })
              .catch(error => {
                this.errorMessage = error.message;
                console.error("There was an error!", error);
              });

            
          });
           setTimeout(() => {
            mediaRecorder.stop();
            this.timerEnabled = false;
            this.timerCount = 5.00; 
            this.recording = false;
          }, 5000);

          stopButton.addEventListener("click", () => {
            this.recording = false

            mediaRecorder.stop();
            this.timerEnabled = false;
             
           
          });
         
        });

      },
  },
};
</script>
<style> 




.pulse {
  color: red;
  animation: pulse 2s infinite;
  margin-right:2%;
  
}
@keyframes pulse {
	0% {
		transform: scale(0.95);
		box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7);
	}

	70% {
		transform: scale(1);
		box-shadow: 0 0 0 10px rgba(255, 0, 0, 0);
	}

	100% {
		transform: scale(0.95);
		box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
	}
}

</style> 