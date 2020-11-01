import flushPromises from 'flush-promises'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import VueBootstrap4Table from 'vue-bootstrap4-table'
import Component from '@/views/Review.vue'
jest.unmock('axios')

const data = [
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
let mockAxios

beforeEach(() => {
  mockAxios = new MockAdapter(axios)
  mockAxios.onGet().reply(200, data)
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
    stubs: ['router-link', 'router-view']
  })
})

afterEach(() => {
  wrapper.destroy()
})

describe('Testing Review component', () => {
  it('is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })
  it('Table is displayed correctly', async () => {
    await flushPromises()
    expect(wrapper.html()).toContain('Miho')
    expect(wrapper.html()).toContain('Mio lesson')
    expect(wrapper.contains('button')).toBe(true)
  })
  it('Approve button calls reviewAction method', async () => {
    await flushPromises()
    // mock reviewAction method
    const reviewAction = jest.fn()
    // updating method with mock function
    wrapper.setMethods({ reviewAction })
    wrapper.find('#approve').trigger('click')
    expect(reviewAction).toBeCalled()
  })
  it('Reject button calls reviewAction method', async () => {
    await flushPromises()
    // mock reviewAction method
    const reviewAction = jest.fn()
    // updating method with mock function
    wrapper.setMethods({ reviewAction })
    wrapper.find('#reject').trigger('click')
    expect(reviewAction).toBeCalled()
  })
  it('reviewAction method is working correctly', async () => {
    await flushPromises()
    wrapper.find('#approve').trigger('click')
    mockAxios.onPut().reply(200)
    mockAxios.onGet().reply(200, [])
    await flushPromises()
    // confirm no result is on table by not existance of button
    expect(wrapper.contains('button')).toBe(false)
  })
})
