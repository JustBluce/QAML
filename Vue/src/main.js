import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import debounce from 'lodash/debounce';
//引入echarts
import echarts from 'echarts';
Vue.prototype.$echarts = echarts;

import 'normalize.css/normalize.css'; // A modern alternative to CSS resets

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/en'; // lang i18n

import vuetify from './plugins/vuetify.js';

import '@/styles/index.scss'; // global css

import App from './App';
import store from './store';
import router from './router';

import firebase from 'firebase';

import '@/icons'; // icon
import '@/permission'; // permission control

import Vuelidate from 'vuelidate'

window._ = require('lodash');

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
if (process.env.NODE_ENV === 'production') {
	const { mockXHR } = require('../mock');
	mockXHR();
}

Vue.use(ElementUI, { locale });
Vue.use(Vuelidate);
Vue.use(VueAxios, axios);

Vue.config.productionTip = false;

new Vue({
	el: '#app',
	vuetify,
	router,
	store,
	render: (h) => h(App)
});

var config = {
	apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
	authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
	projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
	storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
	messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGE_SENDER_ID,
	appID: process.env.VUE_APP_FIREBASE_APPID
  }
  firebase.initializeApp(config)
