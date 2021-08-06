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

firebase
	.auth()
	.setPersistence(firebase.auth.Auth.Persistence.local)
	.then(() => {
		// Existing and future Auth states are now persisted in the current
		// session only. Closing the window would clear any existing state even
		// if a user forgets to sign out.
		// ...
		// New sign-in will be persisted with session persistence.
		var provider = new firebase.auth.GoogleAuthProvider();
		// In memory persistence will be applied to the signed in Google user
		// even though the persistence was set to 'none' and a page redirect
		// occurred.
		return firebase.auth().signInWithRedirect(provider);
	})
	.catch((error) => {
		// Handle Errors here.
		var errorCode = error.code;
		var errorMessage = error.message;
	});
