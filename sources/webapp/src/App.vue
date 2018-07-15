<template>
  <div id="app">
    <!-- Navigation -->
    <b-navbar class="navbar-expand-lg navbar-light bg-white fixed-top" toggleable>
        <b-navbar-nav>
          <b-navbar-brand href="/"><img src="/static/images/geld.tech_32x32.png" width="30" height="30" alt="" /> __PACKAGE_NAME__</b-navbar-brand>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
            <b-nav-form @submit="onSubmit" @reset="onReset">
              <b-form-input id="searchInput" type="search"  v-model="form.keyword" class="form-control mr-sm-2 ml-auto" placeholder="" aria-label="Search"></b-form-input>
              <b-button class="my-2 my-sm-0" variant="primary" type="submit">Search</b-button>
            </b-nav-form>
        </b-navbar-nav>
    </b-navbar>
    <!-- Alerting -->
    <div class="alerting col-md-4 col-md-offset-4">
      <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="error=''" @dismiss-count-down="countDownChanged">
        <p>{{ error }}</p>
      </b-alert>
    </div>
    <!-- Container -->
    <b-container class="bv-example-row">
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h4>Resources</h4>
                <div v-if="loading" class="loading">
                  <img src="/static/images/spinner.gif" width="32" height="32"/>
                </div>
            </b-col>
        </b-row>
    </b-container>
    <div id="app-container">
        <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { fetchData } from '@/api'

export default {
  name: 'App',
  data() {
    return {
      form: {
        keyword: ''
      },
      data: {},
      loading: false,
      dismissCountDown: 0,
      error: '',
      show: true
    }
  },
  created() {
    this.loading = false
    /* Trick to reset/clear native browser form validation state */
    this.data = {}
    this.show = false
    this.$nextTick(() => { this.show = true })
    /* Fetching the data */
    this.loading = true
    fetchData()
      .then(response => {
        this.data = response.data
        this.loading = false
      })
      .catch(err => {
        this.error = err.message
        this.loading = false
      })
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      var searchKeyword = this.sanitizeString(this.form.keyword)
      this.form.keyword = ''
      this.loading = false
      this.dismissCountDown = 0
      this.error = ''
      if (searchKeyword !== '') {
        /* Trick to reset/clear native browser form validation state */
        this.data = {}
        this.show = false
        this.$nextTick(() => { this.show = true })
        /* Fetching the data */
        this.loading = true
        fetchData(searchKeyword)
          .then(response => {
            this.data = response.data
            this.loading = false
          })
          .catch(err => {
            this.error = err.message
            this.loading = false
            this.dismissCountDown = 6
          })
      }
    },
    onReset(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.keyword = ''
      this.data = {}
      this.loading = false
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    },
    sanitizeString(input) {
      input = input.trim()
      input = input.replace(/[`~!$%^&*|+?;:'",\\]/gi, '')
      input = input.replace('/', '')
      input = input.trim()
      return input
    },
    countDownChanged (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 30px;
  padding-top: 50px;
  margin-bottom: 10px;
  padding-bottom: 20px;
}
@media screen and (min-width: 601px) {
  #app {
    margin-top: 5px;
    padding-top: 70px;
    font-size: 24px;
  }
}
@media screen and (max-width: 600px) {
  #app {
    margin-top: 15px;
    margin-bottom: 10px;
    padding-top: 170px;
    font-size: 14px;
  }
}
.alerting {
  margin: 0 auto;
  text-align: center;
  display: block;
  line-height: 15px;
}
.loading {
  width: 50%;
  margin: 0;
  padding-top: 40px;
  padding-left: 40px;
}
.list-no-bullet {
  padding: 0;
  margin: 0;
  list-style-type: none;
}
</style>
