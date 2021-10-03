<!--
Developers: Jason Liu
-->
<template>
  <div>
    <v-switch
      class="my-1"
      hide-details
      v-model="game_mode"
      :label="`Game mode ${game_mode ? 'on' : 'off'}`"
    ></v-switch>

    <v-btn
      :id="'selectTime-' + workspace_id"
      class="my-4"
      block
      :disabled="game_mode"
    >
      <v-icon>mdi-clock-time-four-outline</v-icon>
      <v-spacer></v-spacer>
      {{ menu_time ? "Timer: " + menu_time : "Select time" }}
      <v-spacer></v-spacer>
      <v-menu
        ref="menu"
        v-model="menu"
        transition="scale-transition"
        offset-y
        :activator="'#selectTime-' + workspace_id"
        :disabled="game_mode"
        :close-on-content-click="false"
      >
        <v-time-picker
          v-if="menu"
          v-model="menu_time"
          format="24hr"
          color="primary"
          full-width
          use-seconds
          scrollable
          @input="setTime"
        ></v-time-picker>
      </v-menu>
    </v-btn>

    <vue-countdown :time="time" v-slot="{ hours, minutes, seconds }" @end="end">
      <h2 class="text-h2 font-weight-regular text-center">
        {{ hours }}<span class="px-2">:</span
        >{{ String(minutes).padStart(2, "0") }}<span class="px-2">:</span
        >{{ String(seconds).padStart(2, "0") }}
      </h2>
    </vue-countdown>

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
import VueCountdown from "@chenfengyuan/vue-countdown";

export default {
  name: "Timer",
  props: {
    workspace_id: Number,
  },
  components: {
    VueCountdown,
  },
  data() {
    return {
      time: 5 * 60 * 1000,
      menu: false,
      menu_time: null,
      dialog: false,
    };
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.workspace_id);
    },
    game_mode: {
      get() {
        return this.$store.state.game_mode;
      },
      set(value) {
        this.$store.state.game_mode = value;
      },
    },
  },
  methods: {
    end() {
      this.dialog = true;
      this.axios({
        url: "http://127.0.0.1:5000/func/timeup",
        method: "GET",
      }).then((response) => {
        console.log(response);
      });
    },
    setTime() {
      let times = this.menu_time.split(":");
      this.time = (+times[0] * 60 * 60 + +times[1] * 60 + +times[2]) * 1000;
    },
  },
};
</script>
