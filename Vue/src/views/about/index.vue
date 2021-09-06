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
        <div class="text-h4 font-weight-bold">Cybernetic question writing</div>
        <div class="text-h5 mt-6">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
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
        <div class="text-h5 mt-6">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
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
        <div class="text-h5 mt-6">
          <strong>Developers:</strong>
          Zefan Cai, Atith Gandhi, Jason Liu, Damian Rene, Raj Shah<br />
          <strong>Mentors:</strong>
          Saptarashmi Bandyopadhyay, Jordan Boyd-Graber
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
  min-height: 600px;
  padding: 100px 30vw;
  padding-top: 250px;
}

span {
  color: var(--v-primary-base);
  font-weight: bold;
}

.title {
  min-height: 200px;
  padding: 50px 20vw;
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