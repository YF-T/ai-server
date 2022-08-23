<template>
  <div class="main">
    <el-table :data="indicators" style="width: 1000px;" class="table">
      <el-table-column prop="accessCount" label="执行次数" class="header"/>
      <el-table-column prop="averageResponseTime" label="平均响应时间(ms)" class="header"/>
      <el-table-column prop="minimumResponseTime" label="最小响应时间(ms)" class="header"/>
      <el-table-column prop="maximumResponseTime" label="最大响应时间(ms)" class="header"/>
      <el-table-column prop="firstAccessDate" label="首次访问时间" class="header"/>
      <el-table-column prop="latestAccessDate" label="最新访问时间" class="header"/>
    </el-table>
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
const indicators = ref<FunctionIndicator[]>([])

const store = useStore()

onMounted(() => {
  const deployment = store.state.webname
  const path = `http://127.0.0.1:5000/get_deployment_info/${deployment}`
  const param = new FormData()
  request(path, param).then((res: any) => {
    console.log(res)
    console.log(res.data.output)
    if (res.data.status == 'success') {
      const [
        accessCount,
        averageResponseTime,
        maximumResponseTime,
        minimumResponseTime,
        firstAccessDate,
        latestAccessDate,
      ] = res.data.output
      indicators.value.push({
        accessCount,
        averageResponseTime,
        maximumResponseTime,
        minimumResponseTime,
        firstAccessDate: firstAccessDate || '2022-08-23',
        latestAccessDate: latestAccessDate || '2022-08-23',
      })
    }
  })
})

</script>

<style scoped>
.el-table thead {
  color: black !important; 
}
.main {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

.table {
  display:block;
  margin: 20px;
  height: 400px;
  overflow: auto;
  background: white;
  text-align:center;
  font-size: 20px;
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

</style>