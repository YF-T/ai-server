<template>
  <div>
    <h2>批量任务列表</h2>
    <p>当前服务：{{ service }}</p>
    <p>当前模型：{{ modelName }}</p>
    <el-table>
      <el-table-column prop="taskId" label="任务 ID" >
      <el-table-column prop="taskStatus" label="任务状态" />
      <el-table-column prop="taskStatus" label="操作" >
        <template #default="scope">
        <router-link to="/deploy/test" :params="{ index: scope.$index }">查看</router-link>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script setup lang="ts">
import { ElTable } from 'element-plus'
import { ref } from 'vue'

const service = ref('')
const modelName = ref('')
</script>
<style scoped></style>
