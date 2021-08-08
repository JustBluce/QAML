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

import Vuelidate from 'vuelidate';

window._ = require('lodash');

const firebaseConfig = {
	apiKey: 'AIzaSyAXEuo-gAHpxQ9YxmdDhDK978I4ZDXMPK4',
	authDomain: 'test-login-90a1d.firebaseapp.com',
	projectId: 'test-login-90a1d',
	storageBucket: 'test-login-90a1d.appspot.com',
	messagingSenderId: '199458901110',
	appId: '1:199458901110:web:fc95dd5a9a3ff7c1b36357'
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

firebase.auth().onAuthStateChanged((user) => {
	store.dispatch('fetchUser', user)
});

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
