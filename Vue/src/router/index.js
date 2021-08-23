import Vue from 'vue';
import Router from 'vue-router';
import firebase from 'firebase';

/* Layout */
import Layout from '@/layout';
import Login from '@/views/auth/login.vue';
import Register from '@/views/auth/register.vue';
import PReset from '@/views/auth/PReset.vue';
import About from '@/views/about';
import Tutorial from '@/views/tutorial';
import store from '@/store/index.js';

Vue.use(Router);

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
	{
		path: '/login',
		name: 'Login',
		component: Login,
		hidden: true
	},

	{
		path: '/register',
		name: 'Register',
		component: Register,
		hidden: true
	},
	{
		path: '/password-reset',
		name: 'Password-Reset',
		component: PReset,
		hidden: true
	},

	{
		path: '/about',
		name: 'About',
		component: About,
		hidden: true
	},

	{
		path: '/tutorial',
		name: 'Tutorial',
		component: Tutorial,
		hidden: true
	},

	{
		path: '/404',
		component: () => import('@/views/404'),
		hidden: true
	},

	{
		path: '/',
		component: Layout,
		redirect: '/dashboard',
		children: [
			{
				path: 'dashboard',
				name: 'Dashboard',
				component: () => import('@/views/dashboard/index'),
				meta: { title: 'Dashboard', icon: 'user', requiresAuth: true }
			}
		]
	},

	{
		path: '/qa',
		component: Layout,
		redirect: '/qa',
		children: [
			{
				path: '',
				name: 'QA',
				component: () => import('@/views/QA/index'),
				meta: { title: 'QA', icon: 'form', requiresAuth: true }
			}
		]
	},

	{
		path: '/workspaces',
		component: Layout,
		redirect: '/workspaces',
		children: [
			{
				path: '',
				name: 'Workspaces',
				component: () => import('@/views/workspaces/index'),
				meta: { title: 'Workspaces', icon: 'table', requiresAuth: true }
			}
		]
	},

	// 404 page must be placed at the end !!!
	{ path: '*', redirect: '/404', hidden: true }
];

const createRouter = () =>
	new Router({
		// mode: 'history', // require service support
		scrollBehavior: () => ({ y: 0 }),
		mode: 'history',
		routes: constantRoutes
	});

const router = createRouter();

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
	const newRouter = createRouter();
	router.matcher = newRouter.matcher; // reset router
}

router.beforeEach((to, from, next) => {
	if (to.matched.some((record) => record.meta.requiresAuth)) {
		firebase.auth().onAuthStateChanged((user) => {
			if (user) {
				next();
			} else {
				next('/login');
			}
		});
	} else {
		next();
	}
});

export default router;
