import { compile } from 'vue'
import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import model_info_manage from '../views/model_info_manage.vue'
import login from '../views/login.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/model_info_manage',// 如果要添加新的path，请将该行注释掉,并将下面一行解开注释
    // path: '/infomanage' 
    name: 'infoView',
    component: model_info_manage
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
