import Vue from 'vue'
import Router from 'vue-router'
import { store } from './store.js'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./views/Home.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./components/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('./components/Register.vue')
    },
    {
      path: '/restricted',
      name: 'restricted',
      component: () => import('./views/Restricted.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('./views/Profile.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/log',
      name: 'log',
      component: () => import('./views/AllLog.vue'),
      meta: {
        isAdminlike: true
      }
    },
    {
      path: '/lessonlist',
      name: 'lessonlist',
      component: () => import('./views/LessonList.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/lesson/:lesson_id',
      name: 'lesson',
      component: () => import('./views/Lesson.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/review',
      name: 'review',
      component: () => import('./views/Review.vue'),
      meta: {
        isAdminlike: true
      }
    },
    {
      path: '/error',
      name: 'error',
      component: () => import('./views/Error.vue')
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    // if the user is not loggedin, send to login page
    next('/login')
  } else {
    next()
  }
  if (to.matched.some(record => record.meta.isAdminlike)) {
    if (store.getters.isLoggedIn && store.getters.userPermission) {
      next()
    } else {
      next('/restricted')
    }
  }
})

export default router
