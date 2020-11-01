import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import Component from '@/App.vue'

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(Vuex)
Vue.use(Vuetify)

const router = new VueRouter()

let wrapper
let store
let actions
let mutations
let state
let getters
let vuetify

beforeEach(() => {
  vuetify = new Vuetify()
  actions = {}
  mutations = {}
  state = {
    entries: {
      status: '',
      token: '',
      isAdmin: false,
      userId: null,
      username: null
    }
  }
  getters = {
    entries (state) { return state.entries }
  }
  store = new Vuex.Store({
    actions,
    mutations,
    state,
    getters
  })
  wrapper = shallowMount(Component, {
    store,
    localVue,
    router,
    vuetify,
    stubs: ['router-link', 'router-view'],
    mocks: {
      $http: {
        interceptors: {
          response: {
            use: function () {
              return Promise.resolve({
              })
            }
          }
        }
      }
    },
    computed: {
      isLoggedIn: () => false
    }
  })
})

afterEach(() => {
  wrapper.destroy()
})

describe('Testing App component', () => {
  it('is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })
  it('Non admin user can only see login and register button', () => {
    expect(wrapper.contains('#login')).toBe(true)
    expect(wrapper.contains('#register')).toBe(true)
    expect(wrapper.contains('#logout')).toBe(false)
  })
  it('Loggedin user cant see login and register button but logout button', () => {
    const wrapperAdmin = shallowMount(Component, {
      store,
      localVue,
      router,
      vuetify,
      stubs: ['router-link', 'router-view'],
      mocks: {
        $http: {
          interceptors: {
            response: {
              use: function () {
                return Promise.resolve({
                })
              }
            }
          }
        }
      },
      computed: {
        isLoggedIn: () => true
      }
    })
    expect(wrapperAdmin.contains('#login')).toBe(false)
    expect(wrapperAdmin.contains('#register')).toBe(false)
    expect(wrapperAdmin.contains('#logout')).toBe(true)
  })
})
