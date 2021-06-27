import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import tableRouter from './modules/table'

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
    component: () => import('@/views/login/index'),
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
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Data', icon: 'dashboard' }
    }]
  },

  {
    path: '/friends',
    alwaysShow: true,
    component: Layout,
    redirect: '/friends',
    name: 'Friends',
    meta: { title: 'Tryout Project', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'tset6',
        name: 'test6',
        component: () => import('@/views/friends/test6/index'),
        meta: { title: 'Answer', icon: 'table ' }
      }
    ]
  },


  // {
  //   path: '/user',
  //   alwaysShow: true,
  //   component: Layout,
  //   redirect: '/user',
  //   name: 'Data',
  //   meta: { title: 'Functions', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'user',
  //       name: 'user',
  //       component: () => import('@/views/user/user/index'),
  //       meta: { title: '用户列表', icon: 'table ' }
  //     },
  //     {
  //       path: 'account',
  //       name: 'account',
  //       component: () => import('@/views/user/account/index'),
  //       meta: { title: '用户账户', icon: 'table ' }
  //     },
  //     {
  //       path: 'record',
  //       name: 'record',
  //       component: () => import('@/views/user/record/index'),
  //       meta: { title: '支付记录', icon: 'table ' }
  //     }
  //   ]
  // },







  // {
  //   path: '/store',
  //   alwaysShow: true,
  //   component: Layout,
  //   redirect: '/store',
  //   name: 'Data',
  //   meta: { title: 'Backup', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'store1',
  //       name: 'store1',
  //       component: () => import('@/views/store/store1/index'),
  //       meta: { title: '烧烤摊', icon: 'table ' }
  //     },
  //     {
  //       path: 'store2',
  //       name: 'store2',
  //       component: () => import('@/views/store/store2/index'),
  //       meta: { title: '水果店', icon: 'table ' }
  //     },
  //     {
  //       path: 'store3',
  //       name: 'store3',
  //       component: () => import('@/views/store/store3/index'),
  //       meta: { title: '游戏店', icon: 'table ' }
  //     },
  //   ]
  // },

  // {
  //   path: '/merchant',
  //   alwaysShow: true,
  //   component: Layout,
  //   redirect: '/merchant',
  //   name: 'merchant',
  //   meta: { title: 'User', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'merchant',
  //       name: 'merchant',
  //       component: () => import('@/views/merchant/merchant/index'),
  //       meta: { title: '商家列表', icon: 'table ' }
  //     },
  //     {
  //       path: 'account',
  //       name: 'account',
  //       component: () => import('@/views/merchant/account/index'),
  //       meta: { title: '商家账户', icon: 'table ' }
  //     }
  //   ]
  // },

  tableRouter,

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
