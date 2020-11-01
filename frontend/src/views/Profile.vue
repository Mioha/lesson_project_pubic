<template>
  <v-card class="mx-auto mt-12">
    <v-card-title>
      <h1 class="display-1">Profile</h1>
    </v-card-title>
    <v-card-text class="subtitle-1" id="username">User name {{ username }}</v-card-text>
    <v-card-text>
      <vue-bootstrap4-table :rows="rows" :columns="columns" :config="config">
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
  </v-card>
</template>

<script>
import axios from 'axios'
import VueBootstrap4Table from 'vue-bootstrap4-table'
import moment from 'moment'
import { statusMixin } from '../mixin.js'

export default {
  name: 'ProfilePage',
  mixins: [statusMixin],
  components: {
    VueBootstrap4Table
  },
  data () {
    return {
      rows: [
        {
          name: '',
          start: '',
          end: '',
          status: ''
        }
      ],
      columns: [
        {
          label: 'Lesson name',
          name: 'name',
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
    username: function () {
      return this.$store.getters.username
    }
  },
  created: async function () {
    const resp = await axios.get('/api/v1/users/me/lessonlogs/')
    this.rows = resp.data.map((lessonlog) => {
      return Object.assign(
        {
          name: lessonlog.lesson_id.name,
          start: lessonlog.start_ts,
          end: lessonlog.end_ts,
          status: lessonlog.status
        }
      )
    })
  },
  filters: {
    formatDate: function (date) {
      if (date == null) return
      return moment(date).format('YYYY/MM/DD')
    }
  }
}
</script>

<style>
</style>
