<!--
Developers: Jason Liu
-->

<template>
  <div class="timer">
    <div id="hours">{{ hours }}</div>
    :
    <div id="minutes">{{ minutes }}</div>
    :
    <div id="seconds">{{ seconds }}</div>
  </div>
</template>

<script>
export default {
  name: "Timer",
  data() {
    return {
      hours: "1",
      minutes: "00",
      seconds: "00",
      end: new Date("July 5, 2021 10:10:00").getTime(),
      timer: null,
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
      this.minutes = String(Math.floor(diff / 60 - 60 * this.hours)).padStart(
        2,
        "0"
      );
      this.seconds = String(
        Math.floor(diff - 3600 * this.hours - 60 * this.minutes)
      ).padStart(2, "0");

      if (diff <= 0) {
        this.$store.state.modal.opened = true;
        this.$store.commit("modalText", {
          header: "Time's up !!!",
          body: "Your question is being evaluated.",
        });
        clearInterval(this.timer);
      }
    },
  },
  mounted() {
    this.update();
    this.timer = setInterval(this.update, 1000);
  },
};
</script>

<style scoped>
.timer {
  display: flex;
  flex-direction: row;
  font-size: 64px;
  margin-top: 10px;
}

#hours,
#minutes,
#seconds {
  background-color: rgba(241, 241, 241, 0.98);
  border: none;
  border-radius: 8px;
  width: 85px;
  padding-left: 5px;
  padding-right: 5px;
  text-align: right;
  outline: none;
}
</style>