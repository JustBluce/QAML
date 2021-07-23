<!--
Developers:
Jason Liu
  - Created the Timer
Cai Zefan
  - Make the timer set with 1 hour when first accessed
-->

<template>
  <div class= "timer">
    <div class="timer"  >
      <div id="hours">{{ hours }}</div>
      :
      <div id="minutes">{{ minutes }}</div>
      :
      <div id="seconds">{{ seconds }}</div>
    </div>

    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-card-title>
          {{ workspace.title }}: Time's up
          <v-spacer></v-spacer>
          <v-btn icon @click="dialog = false">
            <v-icon color="red">mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-2">Your question is being evaluated</v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>

export default {
  name: "Timer",
  props: {
    workspace_id: Number,
    widget_id: Number,
  },
  data() {
    return {
      hours: "0",
      minutes: "01",
      seconds: "00",
      end: new Date(new Date().getTime() + 1 * 60 * 1000),
      timer: null,
      time: 20,
      dialog: false,
    };
  },
  computed: {
    workspace() {
      
      return this.$store.getters.workspace(this.workspace_id);
    },
  },
  methods: {
    validate() {
      let hours = parseInt(this.hours);
      let minutes = parseInt(this.minutes);
      let seconds = parseInt(this.seconds);
      if (seconds < 0) {
        seconds = 0;
      }
      if (seconds > 59) {
        minutes += Math.floor(seconds / 60);
        seconds = seconds % 60;
      }
      if (minutes < 0) {
        minutes = 0;
      }
      if (minutes > 59) {
        hours += Math.floor(minutes / 60);
        minutes = minutes % 60;
      }
      if (hours < 0) {
        hours = 0;
      }
      this.hours = String(hours);
      this.minutes = String(minutes).padStart(2, "0");
      this.seconds = String(seconds).padStart(2, "0");
      
    },
    // countdown() {
    //   this.time--;
    //   if (this.time == 0) {
    //     clearInterval(this.timer);
    //   }
    // },
    display(time) {
      this.hours = String(Math.floor(time / 3600));
      this.minutes = String(Math.floor(time / 60 - 60 * this.hours)).padStart(
        2,
        "0"
      );
      this.seconds = String(
        Math.floor(time - 3600 * this.hours - 60 * this.minutes)
      ).padStart(2, "0");
    },
    update() {
      let diff = (this.end - Date.now()) / 1000;
      this.display(diff);
      if (diff <= 0) {
        this.dialog = true;
        this.axios({
          url: "http://127.0.0.1:5000/func/timeup",
          method: "GET",
        }).then((response) => {
          console.log(response);
        });
        clearInterval(this.timer);
        this.display(0);
      }
    },
  },
  mounted() {
    this.timer = setInterval(this.update, 1000);
  },
  // beforeDestroy() {
  //   clearInterval(this.timer);
  // },
};
</script>

<style scoped>
.timer {
  
  display: flex;
  flex-direction: row;
  font-size: 64px;
  line-height: 64px;
  
}

#hours,
#minutes,
#seconds {
  border: none;
  border-radius: 8px;
  width: 85px;
  padding-left: 5px;
  padding-right: 5px;
  text-align: right;
  outline: none;
}
</style>