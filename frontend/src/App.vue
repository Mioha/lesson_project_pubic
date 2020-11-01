<template>
  <v-app id="inspire">
    <v-navigation-drawer app v-model="drawer" clipped>
      <v-container>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title grey--text text--darken-2">
              Navigation lists
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <navi></navi>
      </v-container>
    </v-navigation-drawer>
    <v-app-bar color="primary" dark app clipped-left>
      <v-app-bar-nav-icon @click="drawer=!drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Lesson project</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn class="ma-4" id="login" light v-if="!isLoggedIn" to="/login">Login</v-btn>
      <v-btn id="register" light v-if="!isLoggedIn" to="/register">Register</v-btn>
      <v-btn id="logout" light v-else @click="logout">Logout</v-btn>
    </v-app-bar>
    <v-content>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>
    <v-footer color="primary" dark app>
      made by mm
    </v-footer>
  </v-app>
</template>

<script>
// @ is an alias to /src
import Navi from '@/views/Navi.vue'

export default {
  data () {
    return {
      drawer: null
    }
  },
  components: {
    Navi
  },
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isLoggedIn
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
    },
    checkAdmin: function () {
      this.$store.dispatch('getPerm')
    }
  },
  created: function () {
    // self needs to access this in promise
    const self = this
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function (resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        } if (err.status === 401) {
        } else if (!err.response) {
          // network error
          self.$router.push('/error')
        }
        throw err
      })
    })
  }
}
</script>
