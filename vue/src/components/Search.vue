<template>
  <div class="container-fluid">
    <div>
      <b-card
        header="Pessoas"
        header-tag="header">
        <b-alert
          variant="danger"
          dismissible
          fade
          :show="showAlertError"
          @dismissed="showAlertError=0"
        > {{errMsg}}
        </b-alert>
        <b-form inline>
          <b-input-group>
            <b-form-input id="inputId" v-model="form.id" @blur="getPessoa" placeholder="ID" />
            <b-input-group-append>
              <b-button variant="info" id="showModalButton" @click="showModal()"><font-awesome-icon icon="search" /></b-button>
            </b-input-group-append>
          </b-input-group>
          <b-input-group>
            <b-form-input v-model="form.nome" placeholder="Nome" />
          </b-input-group>
        </b-form>
      </b-card>
    </div>
    <!-- Modal Component -->
    <b-modal ref="searchModal" title="Pesquisar Pessoas">
      <b-alert
        variant="danger"
        dismissible
        fade
        :show="showModalAlertError"
        @dismissed="showModalAlertError=0"
      > {{errMsg}}
      </b-alert>
      <b-form inline>
        <b-input-group>
          <b-form-input v-model="searchForm.nome" type="text" placeholder="Nome" />
          <b-form-input v-model="searchForm.idade" type="text" placeholder="Idade" />
          <b-form-input v-model="searchForm.profissao" type="text" placeholder="Profissão" />
          <b-button id="searchButton" @click="search()" variant="primary">Pesquisar</b-button>
        </b-input-group>
      </b-form>
      <div>
        <b-table
          id="pessoaTable"
          hover
          :items="pessoas"
          @row-dblclicked="dblClickRowHandler"
          @row-clicked="clickRowHandler"
        />
      </div>
      <div slot="modal-footer">
        <b-button :disabled="!this.selectedRow" class="float-right" variant="primary" @click="selectButtonHandler()">Selecionar</b-button>
        <b-button id="hideModalButton" class="float-right" variant="danger" @click="hideModal()">Fechar</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Search',
  mounted () {
    this.search()
  },
  data () {
    return {
      selectedRow: '',
      showSelectButton: false,
      showAlertError: 0,
      showModalAlertError: 0,
      dismissSecsAlert: 3,
      errMsg: '',
      form: {
        id: '',
        nome: ''
      },
      searchForm: {
        nome: '',
        profissao: '',
        idade: ''
      },
      msg: ''
    }
  },
  computed: {
    ...mapState({
      pessoas: state => state.pessoas,
      pessoa: state => state.pessoa
    })
  },
  methods: {
    showModal () {
      this.$refs.searchModal.show()
    },
    hideModal () {
      this.$refs.searchModal.hide()
    },
    clickRowHandler (record, index) {
      this.showSelectButton = true
      this.selectedRow = record
    },
    dblClickRowHandler (record, index) {
      this.form = record
      this.selectedRow = ''
      this.hideModal()
    },
    selectButtonHandler () {
      this.form = this.selectedRow
      this.selectedRow = ''
      this.hideModal()
    },
    search () {
      this.$store.dispatch(
        'list',
        this.searchForm)
        .then(response => {
        })
        .catch(err => {
          this.searchForm.nome = ''
          this.showModalAlertError = 1
          this.errMsg = err.data.message
        })
    },
    getPessoa () {
      let id = this.form.id
      this.$store.dispatch(
        'detail',
        { id })
        .then((res) => {
          this.form.nome = res.result.nome
        })
        .catch(err => {
          this.form.nome = ''
          this.showAlertError = 1
          this.errMsg = err.data.message
        })
    }
  }
}
</script>
