<template>
  <v-card class="mx-auto mt-12">
    <v-card-title>
      <h1 class="display-1">All User Log</h1>
    </v-card-title>
    <v-card-text>
      <vue-bootstrap4-table :rows="rows" :columns="columns" :config="config" v-if="!loading">
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
  name: 'AllLogPage',
  mixins: [statusMixin],
  components: {
    VueBootstrap4Table
  },
  data () {
    return {
      loading: true,
      rows: [
        {
          username: '',
          lessonname: '',
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
          label: 'Lesson Name',
          name: 'lessonname',
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
  created: async function () {
    const resp = await axios.get('/api/v1/lessonlogs/')
    this.rows = resp.data.map((lessonlog) => {
      return Object.assign(
        {
          username: lessonlog.user_id.username,
          lessonname: lessonlog.lesson_id.name,
          start: lessonlog.start_ts,
          end: lessonlog.end_ts,
          status: lessonlog.status
        }
      )
    })
    this.loading = false
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
