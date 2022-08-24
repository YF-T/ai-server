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
    <input type="file" @change="chooseUploadFile" id="fileInput" />
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
const deployment = store.state.webname
const modelName = store.state.modelName
let taskFile: Blob | null = null

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
  const path = `http://127.0.0.1:5000/testmodel_delayresponse/${deployment}`
  const param = new FormData()
  param.append('file', taskFile || '')
  request(path, param).then((res: any) => {
    if (res.status == 'success') {
      tasks.value.push({ taskid: res.taskid })
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
  margin-top: 10px;
}
</style>
