<template>
  <v-container class="mx-auto mt-12"
  max-width="600" fluid>
    <v-row>
      <v-col>
        <v-card class="grey lighten-4" light>
          <v-card-title class="display-1 grey--text text--darken-2">Lesson project</v-card-title>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card v-if="!isAdmin" id="profile">
          <v-card-title>
<router-link to="/profile" class="headline">Profile</router-link></v-card-title>
          <v-card-text class="subtitle-1">
            Let’s check on progress
          </v-card-text>
        </v-card>
        <v-card v-else id="log">
          <v-card-title>
<router-link to="/log" class="headline">All User Log</router-link></v-card-title>
          <v-card-text class="subtitle-1">
            View all user lesson log
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
          <v-card-title>
<router-link to="/lessonlist" class="headline">Lesson List</router-link></v-card-title>
          <v-card-text class="subtitle-1">
            Overview of lessons
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="isAdmin">
        <v-card id="review">
          <v-card-title>
<router-link to="/review" class="headline">Review</router-link></v-card-title>
          <v-card-text class="subtitle-1">
            Approve or Reject lessons
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'Home',
  computed: {
    isAdmin: function () {
      return this.$store.getters.userPermission
    }
  }
}
</script>
