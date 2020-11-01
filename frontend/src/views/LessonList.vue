<template>
  <v-container class="mx-auto mt-12"
  max-width="800" fluid>
    <v-btn class="mb-10 info" v-if="!showForm && isAdmin" @click="showForm = !showForm">Add New Lesson</v-btn>
    <v-form class="mb-10" ref="form" v-if="showForm" v-model="valid" @submit.prevent="postLesson">
      <v-text-field
              v-model="name"
              :rules="[rules.required]"
              label="Name"
              filled
              required
            ></v-text-field>
      <v-text-field
              v-model="number"
              :rules="[rules.required, rules.number]"
              label="Number"
              filled
              required
            ></v-text-field>
      <v-textarea
              v-model="description"
              auto-grow
              :rules="[rules.required]"
              label="Description"
              filled
              required
            ></v-textarea>
      <v-btn class="mr-10 info" :disabled="!valid" @click="postLesson">Create New Lesson</v-btn>
      <v-btn @click="reset">Cancel</v-btn>
    </v-form>
    <v-row>
      <v-col
        v-for="lesson in lessons"
        :key="lesson.id"
        :cols="flex"
      >
        <v-card>
          <v-card-title>
            <h2><router-link :to="{ name: 'lesson', params: { lesson_id: lesson.id }}">{{ lesson.name }}</router-link></h2>
          </v-card-title>
          <v-card-text>
            <p class="mb-6">No. {{ lesson.number }}</p>
            <p style="white-space: pre;" v-html="lesson.description"></p>
            <v-chip class="mt-2" label v-if="!isAdmin">{{ lessonStatus(lesson.status) }}</v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import { statusMixin } from '../mixin.js'

export default {
  name: 'LessonListPage',
  mixins: [statusMixin],
  data () {
    return {
      lessons: [
        {
          id: '',
          name: '',
          number: null,
          description: '',
          status: ''
        }
      ],
      name: '',
      number: null,
      description: '',
      flex: 6,
      showForm: false,
      valid: false,
      rules: {
        required: value => !!value || 'Required.',
        number: v => /^[0-9]{1,2}$/.test(v) || 'This value may contain one or two digits number.'
      }
    }
  },
  computed: {
    isAdmin: function () {
      return this.$store.getters.userPermission
    }
  },
  created: function () {
    this.getData()
  },
  methods: {
    getData: async function () {
      const resp = await axios.get('/api/v1/users/me/lessons/')
      this.lessons = resp.data.map((lessonlog) => {
        return Object.assign(
          {
            id: lessonlog.lesson.id,
            name: lessonlog.lesson.name,
            number: lessonlog.lesson.number,
            description: lessonlog.lesson.description,
            status: lessonlog.lessonlog.status
          }
        )
      })
    },
    postLesson: async function () {
      const options = {
        baseUrl: '/api/v1/lessons_admin/',
        body: {
          name: this.name,
          number: this.number,
          description: this.description
        },
        url () {
          return `${options.baseUrl}`
        }
      }
      await axios({ url: options.url(), data: options.body, method: 'POST' })
      this.getData()
      this.reset()
    },
    reset: function () {
      this.showForm = false
      this.$refs.form.reset()
    }
  }
}
</script>

<style>
</style>
