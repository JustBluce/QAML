<!--
Developers: Atith Gandhi and Jason Liu
-->

<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="answer"
      hide-default-footer
      dense
      class="elevation-2"
    >
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "MachineGuesses",
  props: {
    workspace_id: Number,
  },
  data() {
    return {
      headers: [
        { text: "Machine guess", value: "guess" },
        { text: "Machine score", value: "score" },
      ],
    };
  },
  computed: {
    qa() {
      return this.$store.getters.workspace(this.workspace_id).qa;
    },

    answer() {
      return this.qa.answer;
    },
  },
};
</script>