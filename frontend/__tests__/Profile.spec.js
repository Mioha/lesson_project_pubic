import flushPromises from 'flush-promises'
import axios from 'axios'
import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import VueBootstrap4Table from 'vue-bootstrap4-table'
import Component from '@/views/Profile.vue'

jest.mock('axios', () => ({
  get: () => Promise.resolve({
    data: [
      {
        id: 4,
        start_ts: '2020-06-17T20:29:42.424924+09:00',
        end_ts: '',
        status: 'Under Review',
        user_id: {
          id: 1,
          username: 'Miho'
        },
        lesson_id: {
          id: 1,
          name: 'Mio lesson',
          number: 2,
          description: '7/1 test'
        }
      }
    ]
  })
}))

const localVue = createLocalVue()
localVue.use(VueRouter)
localVue.use(Vuex)
localVue.use(VueBootstrap4Table)
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
  wrapper = mount(Component, {
    store,
    localVue,
    router,
    vuetify,
    stubs: ['router-link', 'router-view'],
    computed: {
      username: () => 'Miho'
    }
  })
})

afterEach(() => {
  wrapper.destroy()
})

describe('Testing Profile component', () => {
  it('is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })
  it('username and table are displayed correctly', async () => {
    await flushPromises()
    expect(wrapper.find('#username').text()).toBe('User name Miho')
    expect(wrapper.html()).toContain('Mio lesson')
    expect(wrapper.html()).toContain('2020/06/17')
    expect(wrapper.html()).toContain('Under Review')
  })
})
