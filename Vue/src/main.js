import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

//引入echarts
import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control

import firebase from "firebase";
import '@firebase/auth';
import '@firebase/firestore';

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../mock')
  mockXHR()
}

// set ElementUI lang to EN
Vue.use(ElementUI, { locale })
Vue.use(VueAxios, axios)
// 如果想要中文版 element-ui，按如下方式声明
// Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})


//firebase config DONT CHANGE FOR NOW
const firebaseConfig = {
  apiKey: "AIzaSyA05i1aGUSmcyhX1jAAXWBpwty9j2OCUu0",
  authDomain: "auth-dc32d.firebaseapp.com",
  projectId: "auth-dc32d",
  storageBucket: "auth-dc32d.appspot.com",
  messagingSenderId: "852543834096",
  appId: "1:852543834096:web:23dc6ae652c54bad853f35"
};
//init firebase and config
firebase.initializeApp(firebaseConfig);



export default firebase; 

