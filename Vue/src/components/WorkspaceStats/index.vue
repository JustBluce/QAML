<!--
Developers: Damian Rene
-->

<template>
  <v-card class="ma-2" style="border-radius: 16px" elevation="4">
    <v-card-title class="background">
      <p class="text mb-0">Overall Statistics</p>
      <v-spacer></v-spacer>
      
    <div>
        
      <v-card class="ma-4">
        <v-card-title>
          Question Statistics
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="genreCount"
          :search="search"
          :sort-by="['Genre', 'Count']"
          :sort-desc="[true, false]"
          multi-sort
        ></v-data-table>
      </v-card>

        </div>
   
   
    <v-card-actions class="pa-4">
    
      <v-btn
        color="primary"
        style="width: 75px"
        text
        outlined
        @click="confirmReset"
      >
        Reset
      </v-btn>
      <v-spacer></v-spacer>
     
    </v-card-actions>

   </v-card-title>
  </v-card>

</template>

<script>

import { GChart } from "vue-google-charts";
import firebase from "firebase";



export default {
  name: "Workspace Stats",
  
  components: {
    GChart,
  },
  data() {
    return {
      user:null ,
      genreCount: [], 
      search: "",
      headers: [
        { text: "Genre", value: "Genre", width: "30%" },
        { text: "Count", value: "Count", width: "30%" }
      ],
       chartData: [
        ['Genre', 'Number of Questions'],
        ['2014', 1000],
        ['2015', 1170],
        ['2016', 660],
        ['2017', 1030]
      ],
    }
  },
  computed:{
    options() {
      return {
        //width: Math.max(1024, this.workspace.style.width) / 3 - 50,
        //backgroundColor: "none",
      };
    },
    methods:{

      mounted() {
        this.user = firebase.auth().currentUser;
        this.axios({
          url: "http://127.0.0.1:5000/genres/getGenre",
          method: "GET",
          params: {
             uid: this.user.uid
        },
        }).then((response) => {
          this.genreCount = response.data;
          console.log(response);
        })
    },



    }
  },
}
</script>
