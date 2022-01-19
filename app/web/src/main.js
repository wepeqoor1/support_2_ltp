import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import Vuex from 'vuex'

import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify)
Vue.use(Vuex)

Vue.config.productionTip = false


const store = new Vuex.Store({
  state: {
    host: 'http://10.49.5.31:8000',
    token: null
  }
})

new Vue({
  render: h => h(App),
  vuetify: new Vuetify(),
  store: store,
}).$mount('#app')
