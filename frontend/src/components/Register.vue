<template>
  <v-card width="400px" class="mx-auto mt-12">
    <v-card-title>
      <h1 class="display-1">Register</h1>
    </v-card-title>
    <v-card-text>
      <v-form v-model="valid" @submit.prevent="register" lazy-validation>
        <v-alert v-if="error" :value="true" type="error" outlined>
            {{ error }}
        </v-alert>
        <v-text-field
                prepend-icon="mdi-account-box"
                v-model="name"
                :rules="[rules.required, rules.username]"
                counter
                label="User Name"
                hint="At least 5 characters"
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
                autocomplete="new-password"
              ></v-text-field>
        <v-text-field
                v-bind:type="showPassword2 ? 'text' : 'password'"
                prepend-icon="mdi-lock"
                v-bind:append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
                v-model="passwordConf"
                :rules="[rules.required, passwordMatch]"
                counter
                label="Confirm Password"
                required
                @click:append="showPassword2 = !showPassword2"
                autocomplete="new-password"
              ></v-text-field>
        <v-card-actions>
          <v-btn class="mr-4 info" :disabled="!valid" @click="register">Register</v-btn>
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
      passwordConf: '',
      showPassword1: false,
      showPassword2: false,
      valid: true,
      rules: {
        required: value => !!value || 'Required.',
        min: v => (v && v.length >= 5) || 'Min 5 characters',
        username: v => /^[\w-]{5,20}$/.test(v) || 'This value may contain min 5 characters. Only letters, numbers, and -/_ characters.'
      },
      error: null
    }
  },
  computed: {
    passwordMatch () {
      return () => this.password === this.passwordConf || 'Password must match'
    }
  },
  methods: {
    register: function () {
      const data = {
        username: this.name,
        password: this.password
      }
      this.$store.dispatch('register', data)
        .then(() => this.$router.push('/login'))
        .catch(err => {
          if (err.response.data.username) {
            this.error = err.response.data.username[0]
          } else {
            this.error = 'Error occured.'
          }
        })
    }
  }
}
</script>
