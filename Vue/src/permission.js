
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
