<template>
<div class="main">

    <el-card style="card" shadow="never">
      <template #header>
      <div class="card_header">
        <span>指标</span>
      </div>
    </template>
    <el-table :data="indicators" stripe style="width: 100%">
    <el-table-column prop="functionName" label="函数名" />
    <el-table-column prop="accessCount" label="访问次数" />
    <el-table-column prop="averageResponseTime" label="平均响应时间(ms)" />
    <el-table-column prop="mediumResponseTime" label="中间响应时间(ms)" />
    <el-table-column prop="minimumResponseTime" label="最小响应时间(ms)" />
    <el-table-column prop="maximumResponseTime" label="最大响应时间(ms)" />
    <el-table-column prop="firstAccessDate" label="首次访问时间" />
    <el-table-column prop="latestAccessDate" label="最新访问时间" />
  </el-table>
 </el-card>
  <el-card style="card" shadow="never">
      <template #header>
      <div class="card_header">
        <span class="fuben">副本</span>
        <el-button :circle="true" size="small" class="count">{{ count }}</el-button>
      </div>
    </template>
    <el-table :data="replicates" stripe style="width: 100%">
    <el-table-column prop="name" label="名称" />
    <el-table-column prop="status" label="状态" />
    <el-table-column prop="operation" label="操作" />
    
    
  </el-table>
 </el-card>
  
</div>
 
</template>

<script lang="ts" setup>
import { ElTable, ElTableColumn, ElCard, ElButton } from 'element-plus'
import { computed } from 'vue'

interface FunctionIndicator {
    functionName: string
accessCount: number 
averageResponseTime: number
mediumResponseTime: number
minimumResponseTime: number
maximumResponseTime: number
firstAccessDate: string
latestAccessDate:  string
}
const indicators: FunctionIndicator[] = [
  {
        functionName: 'predict',
accessCount: 2,
averageResponseTime: 205,
mediumResponseTime: 12,
minimumResponseTime: 398,
maximumResponseTime: 205,
firstAccessDate: '2019-09-28',
latestAccessDate:  '2019-09-28',
  },

]

const replicates = [
    {
        name: 'pmml',
        status: '运行中',
        operation: '...',

    }
]

const count = computed(() => replicates.length)


</script>

<style scoped>
.main {
    background-color: #9cc2e6;
    width: 100%;
    height: 100%;
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

.fuben:after {
    content: '   ';
}
</style>