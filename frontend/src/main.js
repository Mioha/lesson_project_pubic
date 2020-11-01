import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { store, initialState } from './store'

import Axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vuetify from './plugins/vuetify'

Vue.use(BootstrapVue)

Vue.prototype.$http = Axios

// for making vuex state persisted
let savedState = localStorage.getItem('vuex')
savedState = JSON.parse(savedState)

if (savedState !== null && savedState.token !== '') {
  Vue.prototype.$http.defaults.headers.common.Authorization = 'Token ' + savedState.token
}
Vue.prototype.$http.defaults.baseURL = 'http://127.0.0.1:8000'
// don't see unnecessary Vue warnings about production.
Vue.config.productionTip = false

Vue.config.errorHandler = function () {
  router.push('/error')
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App),
  created () {
    // initialState is saved to localStorage when created
    localStorage.setItem('initialState', JSON.stringify(initialState))
  }
}).$mount('#app')
