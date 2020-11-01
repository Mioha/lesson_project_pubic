<template>
  <v-card class="mx-auto mt-12">
    <div v-if="!showForm">
      <v-card-title>
        <h1 class="display-1">{{ name }}</h1>
      </v-card-title>
      <v-card-text>
        <v-chip
        class="mb-6"
        label v-if="!isAdmin"
      >{{ lessonStatus(status) }}
      </v-chip>
      <p class="mb-6">No. {{ number }}</p>
      <p style="white-space: pre;" v-html="description"></p>
      </v-card-text>
    </div>
      <v-card-text>
        <div v-if="isAdmin">
          <v-btn class="mb-10 info" v-if="!showForm" @click="showForm = !showForm">Edit</v-btn>
          <v-form ref="form" v-if="showForm" v-model="valid" @submit.prevent="editLesson" lazy-validation>
            <v-text-field
                    v-model="lesson.name"
                    :rules="[rules.required]"
                    label="Name"
                    filled
                    required
                  ></v-text-field>
            <v-text-field
                    v-model="lesson.number"
                    :rules="[rules.required, rules.number]"
                    label="Number"
                    filled
                    required
                  ></v-text-field>
            <v-textarea
                    v-model="lesson.description"
                    auto-grow
                    :rules="[rules.required]"
                    label="Description"
                    filled
                    required
                  ></v-textarea>
            <v-btn class="mr-10 mb-10 info" :disabled="!valid" @click="editLesson">Save</v-btn>
            <v-btn class="mb-10" @click="reset">Cancel</v-btn>
          </v-form>
        </div>
        <vue-bootstrap4-table :rows="rows" :columns="columns" :config="config" v-if="isAdmin && !loading">
          <template slot="start" slot-scope="props">
            {{ props.cell_value | formatDate }}
          </template>
          <template slot="end" slot-scope="props">
            {{ props.cell_value | formatDate }}
          </template>
          <template slot="status" slot-scope="props">
            {{ lessonStatus(props.cell_value) }}
          </template>
        </vue-bootstrap4-table>
      </v-card-text>
    <v-card-actions>
      <v-btn text color="info" v-if="canStart" v-on:click="startLesson()">Start</v-btn>
      <v-btn text color="info" v-if="canComplete" v-on:click="compLesson()" light>Complete</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios'
import VueBootstrap4Table from 'vue-bootstrap4-table'
import { mapState } from 'vuex'
import moment from 'moment'
import { statusMixin } from '../mixin.js'

export default {
  name: 'LessonPage',
  mixins: [statusMixin],
  components: {
    VueBootstrap4Table
  },
  data () {
    return {
      name: '',
      number: null,
      status: '',
      description: '',
      lesson: {
        name: '',
        number: null,
        description: ''
      },
      loading: true,
      showForm: false,
      valid: true,
      rules: {
        required: value => !!value || 'Required.',
        number: v => /^[0-9]{1,2}$/.test(v) || 'This value may contain one or two digits number.'
      },
      error: null,
      rows: [
        {
          username: '',
          start: '',
          end: '',
          status: ''
        }
      ],
      columns: [
        {
          label: 'User Name',
          name: 'username',
          sort: false
        },
        {
          label: 'Start',
          name: 'start',
          sort: false
        },
        {
          label: 'End',
          name: 'end',
          sort: false
        },
        {
          label: 'Status',
          name: 'status',
          sort: false,
          slot_name: 'status'
        }
      ],
      config: {
        card_mode: false,
        pagination: false, // default true
        pagination_info: false, // default true
        checkbox_rows: false,
        rows_selectable: false,
        card_title: 'Lessons',
        global_search: {
          placeholder: 'Enter custom Search text',
          visibility: false,
          case_sensitive: false
        },
        show_refresh_button: false,
        show_reset_button: false
      }
    }
  },
  computed: {
    canStart: function () {
      return this.status === null
    },
    canComplete: function () {
      return (this.status === 'In Progress' || this.status === 'Not Approved')
    },
    ...mapState([
      'isAdmin',
      'userId'
    ])
  },
  created: function () {
    this.init()
  },
  methods: {
    startLesson: async function () {
      const options = {
        baseUrl: '/api/v1/lessons/',
        id: this.$route.params.lesson_id,
        url () {
          return `${options.baseUrl}${options.id}/start/`
        }
      }
      const resp = await axios({ url: options.url(), data: options.body, method: 'POST' })
      this.status = resp.data.status
    },
    compLesson: async function () {
      const options = {
        baseUrl: '/api/v1/lessons/',
        id: this.$route.params.lesson_id,
        url () {
          return `${options.baseUrl}${options.id}/comp/`
        }
      }
      const resp = await axios({ url: options.url(), data: options.body, method: 'PUT' })
      this.status = resp.data.status
    },
    getData: async function () {
      const options = {
        baseUrl: '/api/v1/users/me/lessons/',
        id: this.$route.params.lesson_id,
        url () {
          return `${options.baseUrl}${options.id}`
        }
      }
      const resp = await axios.get(options.url())
      this.name = resp.data.lesson.name
      this.number = resp.data.lesson.number
      this.description = resp.data.lesson.description
      this.status = resp.data.lessonlog.status
    },
    getDataAdmin: async function () {
      const options = {
        baseUrl: '/api/v1/lessons_admin/',
        id: this.$route.params.lesson_id,
        url () {
          return `${options.baseUrl}${options.id}`
        }
      }
      const resp = await axios.get(options.url())
      this.rows = resp.data.map((lessonlog) => {
        return Object.assign(
          {
            username: lessonlog.user_id.username,
            start: lessonlog.start_ts,
            end: lessonlog.end_ts,
            status: lessonlog.status
          }
        )
      })
      this.name = resp.data[0].lesson_id.name
      this.number = resp.data[0].lesson_id.number
      this.description = resp.data[0].lesson_id.description
      // for lesson edit form
      this.lesson.name = this.name
      this.lesson.number = this.number
      this.lesson.description = this.description
      this.loading = false
    },
    editLesson: async function () {
      const options = {
        baseUrl: '/api/v1/lessons_admin/',
        id: this.$route.params.lesson_id,
        body: {
          lesson_id: this.$route.params.lesson_id,
          name: this.lesson.name,
          number: this.lesson.number,
          description: this.lesson.description
        },
        url () {
          return `${options.baseUrl}${options.id}`
        }
      }
      const resp = await axios({ url: options.url(), data: options.body, method: 'PUT' })
      this.name = resp.data.name
      this.number = resp.data.number
      this.description = resp.data.description
      this.reset()
    },
    reset: function () {
      this.showForm = false
      this.lesson.name = this.name
      this.lesson.number = this.number
      this.lesson.description = this.description
    },
    init: function () {
      // change api to call depends on if admin
      if (!this.isAdmin) {
        // if normal user
        this.getData()
      } else {
        // if admin
        this.getDataAdmin()
      }
    }
  },
  filters: {
    formatDate: function (date) {
      if (date == null) return
      return moment(date).format('YYYY/MM/DD')
    }
  },
  beforeRouteUpdate (to, from, next) {
    // action before rendering
    if (this.showForm) this.reset()
    next()
    // action after rendering
    this.init()
  }
}
</script>

<style>
</style>
