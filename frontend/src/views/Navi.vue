<template>
  <v-list dense shaped>
      <!-- 第1階層 -->
      <v-list-item v-for="nav_list in navList" :key="nav_list.name" :to="nav_list.link">
        <v-list-item-icon>
          <v-icon>{{ nav_list.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>{{ nav_list.name }}</v-list-item-title>
      </v-list-item>
      <!-- 第2階層がある場合 -->
      <v-list-group v-show="isLoggedIn" v-for="navLesson in navLessonList" :key="navLesson.lists.link" :prepend-icon="navLesson.icon"
    no-action :append-icon="navLesson.lists ? undefined : ''">
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>
            <router-link v-bind:to="navLesson.link">{{ navLesson.name }}</router-link>
          </v-list-item-title>
        </v-list-item-content>
      </template>
      <v-list-item v-for="list in navLesson.lists" :key="list.link" :to="list.link">
        <v-list-item-content>
          <v-list-item-title>{{ list.name }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-group>
  </v-list>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Navi',
  data () {
    return {
      navListBase: [
        {
          name: 'Home',
          link: '/',
          icon: 'mdi-home'
        }
      ],
      navList: [
      ],
      navLessonList: [
        {
          name: 'Lessons',
          icon: 'mdi-book-open-page-variant',
          link: '/lessonlist',
          lists: [{
            name: '', link: ''
          }
          ]
        }
      ]
    }
  },
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isLoggedIn
    }
  },
  created: function () {
    if (this.isLoggedIn) this.getData()
    this.makeNav()
  },
  methods: {
    getData: async function () {
      const resp = await axios.get('/api/v1/lessons/')
        .catch(err => {
          if (err.response.status === 401) {
            this.navLessonList[0].lists = {
              name: '', link: ''
            }
          }
        })
      // apply lesson data to navigation
      this.navLessonList[0].lists = resp.data.map((lesson) => {
        return Object.assign(
          {
            name: lesson.name,
            link: '/lesson/' + lesson.id
          }
        )
      })
    },
    makeNav: function () {
      const normUserNav =
        {
          name: 'Profile',
          link: '/profile',
          icon: 'mdi-account'
        }
      const adminUserNav = [
        {
          name: 'All User Log',
          link: '/log',
          icon: 'mdi-account-box-multiple'
        },
        {
          name: 'Review',
          link: '/review',
          icon: 'mdi-check'
        }
      ]
      // change navigation depends on if admin
      if (this.$store.getters.userPermission) {
        this.navList = this.navListBase.concat(adminUserNav)
      } else {
        this.navList = this.navListBase.concat(normUserNav)
      }
    }
  },
  mounted () {
    this.$store.watch(
      (state, getters) => getters.userID,
      () => {
        if (this.isLoggedIn) this.getData()
        this.makeNav()
      }
    )
  }
}
</script>

<style>
</style>
