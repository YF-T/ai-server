<template>
  <div class="main">
      <div>
        <span class="title">指标</span>
      <el-table :data="indicators" style="width: 1000px;" class="table">
        <el-table-column prop="accessCount" label="执行次数" class="header"/>
        <el-table-column prop="averageResponseTime" label="平均响应时间(ms)" class="header"/>
        <el-table-column prop="minimumResponseTime" label="最小响应时间(ms)" class="header"/>
        <el-table-column prop="maximumResponseTime" label="最大响应时间(ms)" class="header"/>
        <el-table-column prop="firstAccessDate" label="首次访问时间" class="header"/>
        <el-table-column prop="latestAccessDate" label="最新访问时间" class="header"/>
      </el-table>
      </div>
      
    <div>
      <span class="title">服务</span>
      <el-table :data="replicates" stripe style="width: 600px;" class="table">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="operation" label="操作">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="toggle(scope.$index)"
            >
              {{
                replicates[scope.$index].status == '运行中' ? '暂停' : '运行'
              }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
      
  </div>
</template>

<script lang="ts" setup>
import { ElTable, ElTableColumn, ElCard, ElButton } from 'element-plus'
import { computed, ref, onMounted } from 'vue'
import { request } from '../Util'
import { useStore } from 'vuex'

interface FunctionIndicator {
  accessCount: number
  averageResponseTime: number
  minimumResponseTime: number
  maximumResponseTime: number
  firstAccessDate: string
  latestAccessDate: string
}
const indicators: FunctionIndicator[] = []

const store = useStore()

onMounted(() => {
  const deployment = store.state.webname
  const path = `http://127.0.0.1:5000/get_deployment_info/${deployment}`
  const param = new FormData()
  request(path, param).then((res: any) => {
    if (res.status == 'success') {
      const [
        accessCount,
        averageResponseTime,
        maximumResponseTime,
        minimumResponseTime,
        firstAccessDate,
        latestAccessDate,
      ] = res.output
      indicators.push({
        accessCount,
        averageResponseTime,
        maximumResponseTime,
        minimumResponseTime,
        firstAccessDate,
        latestAccessDate,
      })
    }
  })
})

const replicates = ref([
  {
    name: 'pmml',
    status: '运行中',
  },
])

const count = computed(() => replicates.value.length)

const toggle = (index: number) => {
  const replicate = replicates.value[index]
  const deploymentName = replicate.name

  const param = new FormData()
  param.append('user', store.state.username)
  param.append('password', store.state.password)
  param.append('modelname', store.state.modelname)
  param.append('deployment', deploymentName)

  if (replicate.status == '运行中') {
    const path = 'http://127.0.0.1:5000/setdeploymentstatuspause'
    request(path, param).then((response: any) => {
      if (response.status == 'success') {
        replicate.status = '已暂停'
      }
    })
  } else if (replicate.status == '已暂停') {
    const path = 'http://127.0.0.1:5000/setdeploymentstatusrunning'
    request(path, param).then((response: any) => {
      if (response.status == 'success') {
        replicate.status = '运行中'
      }
    })
  }
}
</script>

<style scoped>
:root {
  --el-text-color-regular: black;
}
.el-table thead {
  color: black !important; 
}
.main {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 20px;
  margin-top: 20px;
  margin-right: 20px;
  margin-bottom: 20px;
}
.card_header {
  text-align: left;
}

.card {
  width: 100%;
  margin-top: 1em;
  margin-bottom: 1em;
  margin-left: 1em;
  margin-right: 1em;
}

.table {
  flex-grow:1;
  display:block;
  margin: 20px;
  height: 400px;
  overflow: auto;
  background: white;
  text-align:left;
  font-size: large;
  color: black !important;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
  --el-table-header-text-color: black;
  --el-table-text-color: black;
}
.header {
   font-size: large !important;
  color: black !important;
}
.fuben:after {
  content: '   ';
}
</style>