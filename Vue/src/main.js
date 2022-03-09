import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import debounce from 'lodash/debounce';
import VueBlobJsonCsv from 'vue-blob-json-csv';
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
	apiKey: 'AIzaSyBeQWRzGbIiVnHijn_eZrBRbbsuT3N5D0s',
	authDomain: 'question-writing-interface.firebaseapp.com',
	projectId: 'question-writing-interface',
	storageBucket: 'question-writing-interface.appspot.com',
	messagingSenderId: '668025043214',
	appId: '1:668025043214:web:f49afb9f95c5c906907f5f',
	measurementId: 'G-8JMB36KVE8'
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
//firebase.analytics();

var db = firebase.firestore();
db.settings({ timestampsInSnapshots: true });

/* firebase.auth().onAuthStateChanged((user) => {
	store.dispatch('fetchUser', user);
	
	
	
	if(user.emailVerified ){
		store.commit('SET_VERIFIED', true);
		console.log("EMAIL IS VERIFIED:" + store.state.user.verified)
	}
	else{
		store.commit('SET_VERIFIED', false);
	}
});
}); */

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
Vue.use(VueBlobJsonCsv)

new Vue({
	el: '#app',
	vuetify,
	router,
	store,
	render: (h) => h(App)
});
