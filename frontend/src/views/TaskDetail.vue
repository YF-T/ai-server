<template>
  <div class="task_detail">
    <h2>任务详情页面</h2>
    <p>当前模型：{{ modelName }}</p>
    <el-card class="card">
      <p>任务 id: {{ taskId }}</p>
      <p>任务状态: {{ taskStatus }}</p>
      <p>任务结果：</p>
      <CodeViewer :code="result" language="javascript" :key="result"/>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { ElCard } from 'element-plus'
import CodeViewer from '@/components/CodeViewer.vue'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { request } from '../Util'
const route = useRoute()
const store = useStore()

const task = store.state.tasks.find(
  (task: any) => task.taskid == route.params.id
)
const modelName = ref(store.state.modelName)
const deployName = ref(store.state.webname)
const taskId = ref(route.params.id)
const taskStatus = ref(task.status)

onMounted(() => {
  const path = `http://127.0.0.1:5000/get_result_delayresponse/${deployName}/${taskId}`
  const param = new FormData()
  request(path, param).then((res: any) => {
    if (res.data.status == 'success') {

      var str = '\n';
      res.data.output.forEach(element => {
        str += '{\n'
        for(var key in element){
          str += '"'+ key+'":"'+ element[key] + '",\n';
        }
        str +='}';
      });
      result.value = str
      console.log(str);
    }
    else{
      console.log(res.data.status)
    }
  })
})
const result = ref('')
</script>
<style scoped>
.task_detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card {
  width: 50%;
}
</style>
