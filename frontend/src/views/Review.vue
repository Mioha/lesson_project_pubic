<template>
  <v-card class="mx-auto mt-12">
      <v-card-title>
        <h1 class="display-1">Review</h1>
      </v-card-title>
    <v-card-text>
      <vue-bootstrap4-table :rows="rows" :columns="columns" :config="config" v-if="!loading">
        <template slot="approve" slot-scope="props">
          <v-btn class="mr-2" id="approve" small color="primary" v-on:click="reviewAction(props.cell_value.userId, props.cell_value.lessonId, '/api/v1/lessonlogs/approve')">Approve</v-btn>
          <v-btn id="reject" small color="warning" v-on:click="reviewAction(props.cell_value.userId, props.cell_value.lessonId, '/api/v1/lessonlogs/reject')">Reject</v-btn>
        </template>
      </vue-bootstrap4-table>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios'
import VueBootstrap4Table from 'vue-bootstrap4-table'

export default {
  name: 'ReviewPage',
  data () {
    return {
      loading: true,
      rows: [
        {
          username: '',
          name: '',
          action: {
            userId: null,
            lessonId: null
          }
        }
      ],
      columns: [{
        label: 'User Name',
        name: 'username',
        sort: false
      },
      {
        label: 'Lesson Name',
        name: 'name',
        sort: false
      },
      {
        label: 'Approve',
        name: 'action',
        sort: false,
        slot_name: 'approve'
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
  components: {
    VueBootstrap4Table
  },
  created: function () {
    this.getData()
  },
  methods: {
    getData: async function () {
      const options = {
        baseUrl: '/api/v1/lessonlogs/under_review/',
        url () {
          return `${options.baseUrl}`
        }
      }
      const resp = await axios.get(options.url())
      this.rows = resp.data.map((lessonlog) => {
        return Object.assign(
          {
            username: lessonlog.user_id.username,
            name: lessonlog.lesson_id.name,
            action: {
              userId: lessonlog.user_id.id,
              lessonId: lessonlog.lesson_id.id
            }
          }
        )
      })
      this.loading = false
    },
    reviewAction: async function (userId, lessonId, endpoint) {
      const options = {
        baseUrl: endpoint,
        body: {
          user_id: userId,
          lesson_id: lessonId
        },
        url () {
          return `${options.baseUrl}`
        }
      }
      await axios({
        url: options.url(),
        data: options.body,
        method: 'PUT'
      })
      this.getData()
    }
  }
}
</script>

<style>
</style>
