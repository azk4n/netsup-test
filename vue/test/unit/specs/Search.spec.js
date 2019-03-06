import { mount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Search from '@/components/Search'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

const localVue = createLocalVue()
library.add(faSearch)
localVue.use(Vuex)
localVue.use(BootstrapVue)
localVue.component('font-awesome-icon', FontAwesomeIcon)


describe('Search.vue', () => {
  let actions
  let store

  beforeEach(() => {
    // mock das acoes da store
    actions = {
      detail: jest.fn(),
      list: jest.fn()
    }
    store = new Vuex.Store({
      actions
    })
  })

  it('é uma Vue instance', () => {
    const wrapper = mount(Search, { store, localVue })
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
  it('renderiza corretamente', () => {
    const wrapper = mount(Search, { store, localVue })
    expect(wrapper.element).toMatchSnapshot()
  })

  it('aciona action "detail" no @blur do input de ID', () => {
    const wrapper = mount(Search, { store, localVue })
    const input = wrapper.find('#inputId')
    input.element.value = 1
    input.trigger('blur')
    expect(actions.detail).toHaveBeenCalled()
  })

  it('aciona action "list" no @click do botao "Listar"', () => {
    const wrapper = mount(Search, { store, localVue })
    const btn = wrapper.find('#searchButton')
    btn.trigger('click')
    expect(actions.list).toHaveBeenCalled()
  })

  it('botao de "lupa" abre modal', () => {
    // usando spyOn para mockar metodo do componente
    const spy = jest.spyOn(Search.methods, 'showModal');
    const wrapper = mount(Search, { store, localVue })
    const btn = wrapper.find('#showModalButton')
    btn.trigger('click')
    expect(spy).toHaveBeenCalled()
  })

  it('botao "fechar" fecha modal', () => {
    // usando spyOn para mockar metodo do componente
    const spy = jest.spyOn(Search.methods, 'hideModal');
    const wrapper = mount(Search, { store, localVue })
    const btn = wrapper.find('#hideModalButton')
    btn.trigger('click')
    expect(spy).toHaveBeenCalled()
  })

})