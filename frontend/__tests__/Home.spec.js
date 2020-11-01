import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import Component from '@/views/Home.vue'

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
    stubs: ['router-link', 'router-view']
  })
})

afterEach(() => {
  wrapper.destroy()
})

describe('Testing Home component', () => {
  it('is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })
  it('v-card-title is Lesson project', () => {
    expect(wrapper.find('.display-1').text()).toBe('Lesson project')
  })
  it('Non admin user can see profile card and not all user log and review cards', () => {
    expect(wrapper.contains('#profile')).toBe(true)
    expect(wrapper.contains('#log')).toBe(false)
    expect(wrapper.contains('#review')).toBe(false)
  })
  it('Admin user can see all user log and review cards but profile card', () => {
    const wrapperAdmin = shallowMount(Component, {
      localVue,
      router,
      vuetify,
      stubs: ['router-link', 'router-view'],
      computed: {
        isAdmin: () => true
      }
    })
    expect(wrapperAdmin.contains('#profile')).toBe(false)
    expect(wrapperAdmin.contains('#log')).toBe(true)
    expect(wrapperAdmin.contains('#review')).toBe(true)
  })
})
