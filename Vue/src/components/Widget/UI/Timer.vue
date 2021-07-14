<!--
Developers: Jason Liu
  - Created the Timer
Developers: Cai
  - Make the timer set with 1 hour when first accessed
-->

<template>
  <div ref="timerContainer">
    <div class="timer">
      <div id="hours">{{ hours }}</div>
      :
      <div id="minutes">{{ minutes }}</div>
      :
      <div id="seconds">{{ seconds }}</div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import Modal from "@/components/Modal";
export default {
  name: "Timer",
  data() {
    return {
      hours: "0",
      minutes: "05",
      seconds: "00",
      end: new Date(new Date().getTime() + 5 * 60 * 1000),
      timer: null,
      time: 20,
    };
  },
  mounted() {
    this.timer = setInterval(this.update, 1000);
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
        this.addModal("Time's up !!!", "Your question is being evaluated.");
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
    addModal(header, body) {
      let ModalClass = Vue.extend(Modal);
      let modal = new ModalClass({
        propsData: { header, body },
      });
      modal.$mount();
      this.$refs.timerContainer.appendChild(modal.$el);
    },
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