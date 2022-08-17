import { compile } from 'vue'
import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import model_info_manage from '../views/model_info_manage.vue'
import login from '../views/login.vue'
import DeployDetail from '../views/DeployDetail.vue'
import DeployTest from '../views/DeployTest.vue'
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/model_info_manage',
    name: 'infoView',
    component: model_info_manage
  },
  {
    path: '/deploy/info', 
    name: 'deployInfo',
    component: DeployDetail
  },
  {
    path: '/deploy/test', 
    name: 'deployTest',
    component: DeployTest
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
