<template>
  <v-menu bottom rounded offset-y>
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-avatar size="36px">
          <img
            v-if="user.photoURL"
            :src="user.photoURL"
            style="
              width: 35px;
              height: 35px;
              border-radius: 50%;
              border: 2px solid #333;
            "
          />
          <v-icon v-else>mdi-account-circle</v-icon>
        </v-avatar>
      </v-btn>
    </template>
    <v-card>
      <v-list-item-content class="justify-center">
        <div class="mx-auto text-center">
          <h3 class="pa-2">{{ user.name }}</h3>
          <v-divider class="my-1"></v-divider>
          <v-btn depressed rounded text href="/"> Home </v-btn>
          <v-divider class="my-1"></v-divider>
          <v-btn
            depressed
            rounded
            text
            target="_blank"
            href="https://github.com/JustBluce/TryoutProject"
          >
            GitHub
          </v-btn>
          <v-divider class="my-1"></v-divider>
          <v-btn depressed rounded text @click.native="logout"> Logout </v-btn>
        </div>
      </v-list-item-content>
    </v-card>
  </v-menu>
</template>

<script>
import firebase from "firebase";

export default {
  name: "Profile",
  data() {
    return {
      user: null,
    };
  },
  created() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        this.user = user;
      }
    });
  },
  methods: {
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    },
  },
  async mounted() {
    this.user = await this.$store.dispatch("user/getInfo");
  },
};
</script>