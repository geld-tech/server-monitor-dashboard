// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import BootstrapVue from 'bootstrap-vue'
import { Alert, Collapse, Navbar } from 'bootstrap-vue/es/components'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(Alert)
Vue.use(Collapse)
Vue.use(Navbar)

Vue.config.productionTip = false

var vm = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
vm.$mount('#main')
