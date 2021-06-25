<!--
Developer: Jason Liu
-->

<template>
  <div id="timer">
    <input id="hours" v-model="hours" type="number" />:
    <input id="minutes" v-model="minutes" type="number" />:
    <input id="seconds" v-model="seconds" type="number" />
  </div>
</template>

<script>
export default {
  name: "Timer",
  props: {
    end: Number,
  },
  data() {
    return {
      hours: "1",
      minutes: "00",
      seconds: "00",
    };
  },
  methods: {
    /* validate() {
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
    }, */

    update() {
      let diff = (this.end - Date.now()) / 1000;
      this.hours = String(Math.floor(diff / 3600));
      this.minutes = String(
        Math.floor(diff / 60 - 60 * this.hours)
      ).padStart(2, "0");
      this.seconds = String(
        Math.floor(diff - 3600 * this.hours - 60 * this.minutes)
      ).padStart(2, "0");
    },
  },
  mounted() {
    this.update();
    setInterval(this.update, 1000);
  },
};
</script>

<style scoped>
#timer {
  display: flex;
  flex-direction: row;
  width: 400px;
  font-size: 80px;
  margin-top: 10px;
}

input {
  background-color: rgba(241, 241, 241, 0.98);
  border: none;
  border-radius: 8px;
  width: 120px;
  text-align: right;
  outline: none;
}
</style>