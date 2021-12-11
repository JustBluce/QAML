<!--
Developers: Jason Liu
-->
<template>
  <v-container
    fluid
    class="pa-0"
    style="height: calc(100vh - 64px); overflow: auto"
  >
    <v-container fluid class="pa-0">
      <section class="title background">
        <div class="text-h2 font-weight-bold">QAML</div>
        <div class="text-body-1 font-italic">/ˈkæməl/</div>
        <div class="text-h5 mt-2">
          <span>Q</span>uestion-writing <span>A</span>ided by
          <span>M</span>achine <span>L</span>earning
        </div>
      </section>
      <section class="primary">
        <div class="text-h4 font-weight-bold">Adversarial question writing</div>
        <div class="text-justify mt-6 par">
          Whether you are a professional Quiz Bowl writer, or just new to
          playing trivia games, the Trick interface helps you unlock the full
          potential of your question writing skills. In order to assist users,
          Trick has a suite of interactive machine-learning tools working in
          real time, including our AI’s buzz position, top guesses, giveaway
          clues, and more. Additional widgets aim to assist users in improving
          question diversity by recommending relevant yet underrepresented
          topics, and identifying similar phrases from past questions. Users can
          download their trivia questions which can help them while practicing
          for trivia competitions. Combining the robustness of machine models
          with the ingenuity of human creativity, we can make question-answering
          an exciting community for all while improving the paradigms of
          adversarial learning.
        </div>
        <div class="wave">
          <svg
            data-name="Layer 1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
          >
            <path
              d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
              class="background-fill"
            ></path>
          </svg>
        </div>
      </section>
      <section class="background">
        <div class="text-h4 font-weight-bold">AI-enhanced gameplay</div>
        <div class="text-justify mt-6 par">
          Play with your friends against the timer to write the most adversarial
          trivia question you can in 5 minutes! Trick incentivizes adversarial
          question-writing by rewarding users with points for submitting
          questions that our AI finds difficult and diverse. Characteristics of
          an adversarial question include late or incorrect machine buzzes,
          novel clues, and inclusion of underrepresented entities. Points and
          high leaderboard positions can be exchanged for prizes.
        </div>
        <div class="wave">
          <svg
            data-name="Layer 1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
          >
            <path
              d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
              class="primary-fill"
            ></path>
          </svg>
        </div>
      </section>
      <section class="primary">
        <div class="text-h4 font-weight-bold">Meet the team</div>
        <div class="mt-6 par">
          <strong>Developers:</strong>
          <ul>
            <li>Saptarashmi Bandyopadhyay (University of Maryland)</li>
            <li>Raj Shah (Georgia Institute of Technology)</li>
            <li>Atith Gandhi</li>
            <li>Zefan Cai (Peking University)</li>
            <li>Jason Liu (Montgomery Blair High School)</li>
            <li>Damian Rene (The Gunston School)</li>
            <li>Dr. Jordan Boyd-Graber (University of Maryland)</li>
          </ul>
        </div>
        <div class="wave">
          <svg
            data-name="Layer 1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
          >
            <path
              d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
              class="background-fill"
            ></path>
          </svg>
        </div>
      </section>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: "About",
};
</script>

<style scoped>
section {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 200px;
  padding: 50px;
  padding-top: 200px;
}
span {
  color: var(--v-primary-base);
  font-weight: bold;
}
.title {
  min-height: 100px;
  padding: 50px 20vw;
}
.par {
  width: 600px;
  font-size: 1.25em;
}
.wave {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
}
.wave svg {
  position: relative;
  display: block;
  width: calc(131% + 1.3px);
  height: 300px;
}
.wave .background-fill {
  fill: var(--v-background-base);
}
.wave .primary-fill {
  fill: var(--v-primary-base);
}
</style>