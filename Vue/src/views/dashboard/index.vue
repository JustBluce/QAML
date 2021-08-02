<template>
  <v-main>
    <Taskbar title="Dashboard" />
    <v-container fluid>
      <h1>Adversarial Trivia Question Writing Interface</h1>
      <p style="font-size: 20px">
        <span class="font-weight-bold">Developers:</span>
        Zefan Cai, Atith Gandhi, Jason Liu, Damian Rene, Raj Shah
      </p>
      <p style="font-size: 20px">
        <span class="font-weight-bold">Mentors:</span>
        Saptarashmi Bandyopadhyay, Jordan Boyd-Graber
      </p>
    </v-container>
  </v-main>
</template>

<script>
import Taskbar from "@/components/Taskbar";

export default {
  name: "Dashboard",
  components: {
    Taskbar,
  },
};
</script>
