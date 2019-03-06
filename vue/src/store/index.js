import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)

const initialState = {
  pessoa: '',
  pessoas: [],
  error: '',
  loading: false
}

const getters = {
}

const actions = {
  list ({ commit }, searchForm) {
    const path = `http://localhost:5000/pessoas`
    commit('LOADING')
    return new Promise((resolve, reject) => {
      axios.post(path, searchForm, {headers: {'Authorization': 'test'}})
        .then(({ data }) => {
          commit('LIST', data)
          resolve(data)
        })
        .catch(e => {
          commit('ERROR', e)
          reject(e.response)
        })
    })
  },
  detail ({ commit }, { id }) {
    commit('LOADING')
    const path = `http://localhost:5000/pessoas/${id}`
    return new Promise((resolve, reject) => {
      axios.get(path, {headers: {'Authorization': 'test'}})
        .then(({ data }) => {
          commit('SET', data)
          resolve(data)
        })
        .catch(e => {
          commit('ERROR', e)
          reject(e.response)
        })
    })
  }
}

const mutations = {
  LOADING (state, data) {
    state['loading'] = true
  },
  LIST (state, data) {
    state['loading'] = false
    state['pessoas'] = data.result
  },
  SET (state, data) {
    state['loading'] = false
    state['pessoa'] = data
  },
  ERROR (state, e) {
    state['loading'] = false
    state['error'] = e
  }
}

const store = new Vuex.Store({
  state: initialState,
  getters,
  actions,
  mutations
})

export default store
