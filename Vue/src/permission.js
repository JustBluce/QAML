

import router from './router';
import store from './store';
import { Message } from 'element-ui';
import NProgress from 'nprogress'; // progress bar
import 'nprogress/nprogress.css'; // progress bar style
import { getToken } from '@/utils/auth'; // get token from cookie
import getPageTitle from '@/utils/get-page-title';
import firebase from 'firebase'


NProgress.configure({ showSpinner: false }); // NProgress Configuration

const whiteList = [ '/login' ]; // no redirect whitelist

//Router Guarding Damian Rene
router.beforeEach((to, from, next) => {

	if (to.matched.some(record => record.meta.auth)) {
	  firebase.auth().onAuthStateChanged(user => {
		if (user) {
		  next()
		} else {
		  next({
			path: "/login",
		  })
		}
	  })
	} else if (to.matched.some(record => record.meta.guest)) {
	  firebase.auth().onAuthStateChanged(user => {
		if (user) {
		  next({
			path: "/dashboard",
		  })
		} else {
		  next()
		}
	  })
  
	} else {
	  next()
	}
  
  })
