<template>
  <v-card width="400px" class="mx-auto mt-12">
    <v-card-title>
      <h1 class="display-1">Login</h1>
    </v-card-title>
    <v-card-text>
      <v-form v-model="valid" @submit.prevent="login" lazy-validation>
        <v-alert v-if="error" :value="true" type="error" outlined>
            {{ error }}
        </v-alert>
        <v-text-field
                prepend-icon="mdi-account-box"
                v-model="name"
                :rules="[rules.required]"
                counter
                label="User Name"
                required
                autocomplete="username"
              ></v-text-field>
        <v-text-field
                v-bind:type="showPassword1 ? 'text' : 'password'"
                prepend-icon="mdi-lock"
                v-bind:append-icon="showPassword1 ? 'mdi-eye' : 'mdi-eye-off'"
                v-model="password"
                :rules="[rules.required, rules.min]"
                counter
                label="Password"
                hint="At least 5 characters"
                required
                @click:append="showPassword1 = !showPassword1"
                autocomplete="current-password"
              ></v-text-field>
        <v-card-actions>
          <v-btn class="mr-4 info" :disabled="!valid" @click="login">Login</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      name: '',
      password: '',
      showPassword1: false,
      valid: true,
      rules: {
        required: value => !!value || 'Required.',
        min: v => (v && v.length >= 5) || 'Min 5 characters'
      },
      error: null
    }
  },
  methods: {
    login: function () {
      const username = this.name
      const password = this.password
      this.$store.dispatch('login', {
        username,
        password
      })
        .then(() => {
          this.$router.push('/')
          this.$store.dispatch('getPerm')
        })
        .catch(err => {
          if (err.response.status === 400) {
            this.error = 'User Name or Password is wrong.'
          } else {
            this.error = 'Error occured.'
          }
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style lang="scss" scoped>
</style>
