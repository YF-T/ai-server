<template>
  <div class="main">
    <h2>批量任务列表</h2>
    <el-table :data="tasks" style="width: 50%">
      <el-table-column prop="taskid" label="任务 ID" />
      <el-table-column prop="taskid" label="操作">
        <template #default="scope">
          <el-button @click="gotoDetail(scope.$index)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="fileup">
      <label>训练文件上传:</label><input type="file" @change="chooseUploadFile1" class="fileInput" />
    </div>
    <div class="fileup">
      <label>预处理代码上传:</label><input type="file" @change="chooseUploadFile2" class="fileInput" />
    </div>
    <el-button @click="update" class="upload">上传</el-button>
  </div>
</template>
<script setup lang="ts">
import { ElTable, ElButton, ElTableColumn } from 'element-plus'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { request } from '../Util'
import { useRouter } from 'vue-router'
const store = useStore()
const deployment = ref(store.state.webname)
const modelName = ref(store.state.modelname)
let taskFile1: Blob | null = null
let taskFile2: Blob | null = null

interface Task {
  taskid: string
}
const tasks = ref<Task[]>([])

const router = useRouter()

const gotoDetail = (index: number) => {
  const id = tasks.value[index].taskid
  router.push(`/deploy/tasks/${id}`)
}

onMounted(() => {
  const path = `http://127.0.0.1:5000/getdeploymenttask`
  const param = new FormData()
  param.append('user', store.state.user)
  param.append('password', store.state.password)
  param.append('deployment', deployment)
  
  request(path, param).then((res: any) => {
    if (res.data.status == 'success') {
      console.log(res.data.taskid)
      tasks.value = [...res.data.taskid.map((i: string) => ({ taskid: i }))]
      store.commit('savetasks', tasks)
    }
  })
})

const update = () => {
  const path = `http://127.0.0.1:5000/testmodel_delayresponse/${deployment.value}`
  const param = new FormData()
  param.append('file', taskFile1 || '')
  param.append('prepare_py', taskFile2 || '')
  console.log(taskFile1, taskFile2)
  request(path, param).then((res: any) => {
    if (res.data.status == 'success') {
      alert('已添加新任务')
      tasks.value.push({ taskid: res.data.taskid })
    } else if (res.status == 'runtime error') {
      alert('运行时错误')
    } else if (res.status == 'model not found') {
      alert('模型不存在')
    } else if (res.status == 'preprocess failed') {
      alert('预处理失败，请检查语法')
    }
  })
}

const chooseUploadFile1 = (e: any) => {
  const file = e.target.files.item(0)
  if (!file) return
  taskFile1 = file
  // 清空，防止上传后再上传没有反应
  e.target.value = ''
}

const chooseUploadFile2 = (e: any) => {
  const file = e.target.files.item(0)
  if (!file) return
  taskFile2 = file
  // 清空，防止上传后再上传没有反应
  e.target.value = ''
}
</script>
<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  /* justify-content: center; */
  margin-top: 100px;
  margin-left: 200px;
  margin-right: 200px;
  height: 600px;
  margin-bottom: 100px;
  border: 4px solid rgb(179, 191, 231);
  border-radius: 10px;
}

.upload {
  margin-top: 40px;
}

div[class="fileup"]{
  position: relative;
  top:20px;
  left:100px;
  display: flex;
  flex-direction: row;
  line-height: 50px;
  
}

input[class="fileInput"]{
  display: block;
  margin: 10px 20px;
}
</style>
