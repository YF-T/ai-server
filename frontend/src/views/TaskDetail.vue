<template>
  <div class="task_detail">
    <h2>任务详情页面</h2>
    <p>当前服务：{{ service }}</p>
    <p>当前模型：{{ modelName }}</p>
    <el-card class="card">
        <p>任务 id: {{ taskId }}</p>
        <p>任务状态: {{ taskState }}</p>
        <p>任务结果：</p>
        <CodeViewer :code="result" language="javascript"/>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { ElCard } from 'element-plus'
import CodeViewer from '@/components/CodeViewer.vue';
import { ref } from 'vue'

const service = ref('')
const modelName = ref('')
const taskId= ref('')
const taskState = ref('')
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