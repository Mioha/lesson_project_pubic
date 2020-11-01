import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export const initialState = {
  status: '',
  token: '',
  isAdmin: false,
  userId: null,
  username: null
}

export const store = new Vuex.Store({
  state: initialState,
  mutations: {
    auth_request (state) {
      state.status = 'loading'
    },
    auth_success (state, token) {
      state.status = 'success'
      state.token = token
    },
    user_admin (state, user) {
      state.isAdmin = user.admin
      state.userId = user.id
      state.username = user.username
    },
    auth_error (state) {
      state.status = 'error'
      state.token = ''
    },
    logout (state) {
      Object.assign(state, JSON.parse(localStorage.getItem('initialState')))
      state.token = ''
    }
  },
  actions: {
    login ({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: '/api/v1/login/', data: user, method: 'POST' })
          .then(resp => {
            const token = resp.data.token
            axios.defaults.headers.common.Authorization = 'Token ' + token
            commit('auth_success', token)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')
            reject(err)
          })
      })
    },
    getPerm ({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/v1/users/me/')
          .then(resp => {
            commit('user_admin', { id: resp.data.user_id, admin: resp.data.is_admin, username: resp.data.username })
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    register ({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: '/api/v1/register/', data: user, method: 'POST' })
          .then(resp => {
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error', err)
            reject(err)
          })
      })
    },
    logout ({ commit }) {
      return new Promise((resolve, reject) => {
        commit('logout')
        delete axios.defaults.headers.common.Authorization
        resolve()
      })
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userPermission: state => state.isAdmin,
    userID: state => state.userId,
    username: state => state.username
  },
  plugins: [createPersistedState()]
})
