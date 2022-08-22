import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import model_info_manage from '../views/model_info_manage.vue'
import login from '../views/login.vue'
import DeployDetail from '../views/DeployDetail.vue'
import DeployTest from '../views/DeployTest.vue'
import model_manage from '../views/model_manage.vue'
import newmodel from  '../views/newmodel.vue'
import BatchTaskList from '../views/BatchTaskList.vue'
import TaskDetail from '../views/TaskDetail.vue'
import Deploysum from '../views/Deploysum.vue'
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
  },
  {
    path: "/deploy",
    name: "deploysum",
    component: Deploysum,
    children: [
      {
        // path: '/deploy/info', 
        path: '/deploy/', 
        name: 'deployInfo',
        component: DeployDetail
      },
      {
        path: '/deploy/test', 
        name: 'deployTest',
        component: DeployTest
      },  
      {
        path: '/deploy/tasks', 
        name: 'tasks',
        component: TaskDetail,
      },
    ]
  },
  {
    path: '/model_manage',
    name: 'model_manage',
    component: model_manage
  },
  {
    path: '/newmodel',
    name: 'newmodel',
    component: newmodel
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
