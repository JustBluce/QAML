<!--
Developers:
Jason Liu
  - Created the Timer
Cai Zefan
  - Make the timer set with 1 hour when first accessed
-->

<template>
  <div>
    <v-switch
      class="my-2"
      hide-details
      v-model="game_mode"
      :label="`Game mode ${game_mode ? 'on' : 'off'}`"
    ></v-switch>

    <vue-countdown :time="time" v-slot="{ hours, minutes, seconds }" @end="end">
      <h2 class="text-h2 font-weight-regular text-center">
        {{ hours }} : {{ String(minutes).padStart(2, "0") }} :
        {{ String(seconds).padStart(2, "0") }}
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
  },
  mounted() {
    console.log(this.time);
  },
};
</script>
