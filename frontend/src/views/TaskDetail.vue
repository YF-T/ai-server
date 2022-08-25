<template>
  <div class="task_detail">
    <h2>任务详情页面</h2>
    <el-card class="card">
      <p>任务 id: {{ taskId }}</p>
      <p>任务结果：</p>
      <CodeViewer :code="result" language="javascript" :key="result"/>
    </el-card>
    <div class="button">
      <button @click="reback"><span>返回</span></button>
    </div>
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
const modelName = ref(store.state.modelname)
const deployName = ref(store.state.webname)
const taskId = ref(route.params.id)
const taskStatus = ref(task.status)

const router = useRouter()

const reback = () => {
  router.push(`/deploy/tasks`)
}

onMounted(() => {
  const path = `http://127.0.0.1:5000/get_result_delayresponse/${deployName.value}/${taskId.value}`
  const param = new FormData()
  request(path, param).then((res: any) => {
    if (res.data.status == 'success') {
      console.log(res.data.output);
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

.button{
  display: flex;
  justify-content: center;
}

button{
  position: relative;
  top:8px;
  border: none;
  display: inline-block;
  padding: 10px 30px;

  margin: 0px 20px;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 2px;
  color:#5a94a2;
  border-radius: 40px;
  box-shadow: -2px -2px 8px rgba(255, 255, 255, 1),-2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),2px 2px 8px rgba(0, 0, 0, 0.15);
}

button:hover{
  box-shadow: inset -2px -2px 8px rgba(255, 255, 255, 1),inset -2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),inset 2px 2px 8px rgba(0, 0, 0, 0.15);
}

button:hover:span{
  display: inline-block;
  transform: scale(0.98);
}
</style>
