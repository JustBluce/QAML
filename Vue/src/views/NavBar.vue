<!--
Developers: Damian Rene and Jason Liu
--> 
 
<template>
  <v-app-bar app>
    <v-toolbar-title style="font-size: 24px"> QAML </v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items>
      <v-btn
        v-for="item in items"
        :key="item.title"
        :to="item.link"
        min-width="125"
        max-width="125"
      >
        <v-icon left>{{ item.icon }}</v-icon>
        {{ item.title }}
      </v-btn>
    </v-toolbar-items>

    <v-btn
      id="toggleTheme"
      icon
      large
      class="ml-2 mr-1"
      @click="$vuetify.theme.dark = !$vuetify.theme.dark"
    >
      <v-icon>mdi-brightness-6</v-icon>
      <v-tooltip bottom activator="#toggleTheme">
        <span v-if="$vuetify.theme.dark">Light mode</span>
        <span v-else>Dark mode</span>
      </v-tooltip>
    </v-btn>

    <Profile :navbar="true" />
  </v-app-bar>
</template>

<script>
import Profile from "@/components/Profile";

export default {
  components: {
    Profile,
  },
  computed: {
    items() {
      let menuItems = [
        {
          title: "Login",
          icon: "mdi-login-variant",
          link: "/login",
        },
        {
          title: "Register",
          icon: "mdi-account-plus-outline",
          link: "/register",
        },
        {
          title: "About",
          icon: "mdi-information-outline",
          link: "/about",
        },
        {
          title: "Tutorial",
          icon: "mdi-school-outline",
          link: "/tutorial",
        },
      ];
      return menuItems;
    },
  },
};
</script>
