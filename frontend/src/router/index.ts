import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import DeployTest from '../views/DeployTest.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'deploydetail',
    component: DeployTest
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
