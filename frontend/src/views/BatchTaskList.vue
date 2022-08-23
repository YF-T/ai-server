<template>
  <div>
    <h2>批量任务列表</h2>
    <p>当前模型：{{ modelName }}</p>
    <el-table :data="tasks">
      <el-table-column prop="taskId" label="任务 ID" >
      <el-table-column prop="taskStatus" label="任务状态" />
      <el-table-column prop="taskStatus" label="操作" >
        <template #default="scope">
        <router-link to="/deploy/test" :params="{ index: scope.$index }">查看</router-link>
        </template>
      </el-table-column>
      <input type="file" @change="chooseUploadFile" id="fileInput" />
    </el-table>
<el-button @click="update">更新</el-button>
  </div>
</template>
<script setup lang="ts">
import { ElTable, ElButton } from 'element-plus'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { request } from '../Util'
const store = useStore()
const deployment = store.state.webname
const modelName = store.state.modelName
let taskFile: Blob | null = null

const tasks: any[] = []
const update = () => {
 const path = `http://127.0.0.1:5000/testmodel_delayresponse/${deployment}`
  const param = new FormData()
  param.append('file',taskFile || '')
  request(path, param).then((res: any) => {
    if (res.status == 'success') {
      tasks.push({taskid: res.taskid, status: 'running'})
    } else if (res.status == 'runtime error') {
      alert('运行时错误')
    } else if (res.status == 'model not found') {
      alert('模型不存在')
    } else if (res.status == 'preprocess failed') {
      alert('预处理失败，请检查语法')
    }
  })
}
const chooseUploadFile = (e: any) => {
  const file = e.target.files.item(0).getAsFile()
  if (!file) return
  taskFile = file
  // 清空，防止上传后再上传没有反应
  e.target.value = ''
}


</script>
<style scoped></style>
