import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import Component from '@/views/Restricted.vue'

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

beforeEach(() => {
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
    stubs: ['router-link']
  })
})

afterEach(() => {
  wrapper.destroy()
})

describe('Testing Restricted component', () => {
  it('is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })
  it('title is correct', () => {
    expect(wrapper.find('.display-1').text()).toBe('This page is protected by auth')
  })
})
