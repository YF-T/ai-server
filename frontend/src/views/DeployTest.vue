<template>
  <div>
    <div class="details">
        <div>端点:<el-tag>POST</el-tag></div>
        <div>部署令牌</div>
    </div>
    
    <el-card style="card" shadow="never">
      <template #header>
        <div class="card_header">
          <span>请求</span>
          <el-link type="primary" @click="() => dialogVisible = true">生成代码</el-link>
        </div>
      </template>
      <el-form :model="form" label-position="top" :rules="rules" ref="formRef">
        <el-form-item label="函数名" prop="functionName">
          <el-input v-model="form.functionName"></el-input>
        </el-form-item>
        <el-form-item label="请求" prop="request">
          <el-input v-model="form.request"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button-group>
            <el-button @click="clear">清除</el-button>
            <el-button @click="submit" type="primary">提交</el-button>
          </el-button-group>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="card" shadow="never">
      <template #header>
        <div class="card_header">
          <span>响应</span>
          
        </div>
      </template>
      <code>{{ response }}</code>
    </el-card>

    <el-dialog :model="dialogVisible">
    <p>生成代码</p>
    <div>some code</div>
    <!-- todo:introduce code editor -->
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import {
  ElCard,
  ElLink,
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElButtonGroup,
  ElDialog,
  ElTag,
} from 'element-plus'
import { reactive, ref } from 'vue'
import type { FormRules, FormInstance } from 'element-plus'
const handleClick = () => {

}
const form = reactive({
  functionName: '',
  request: '',
})

const formRef = ref<FormInstance>()
const rules = reactive<FormRules>({
  functionName: [{ required: true, message: '请填写函数名', trigger: 'blur' }],
  request: [{ required: true, message: '请填写请求', trigger: 'blur' }],
})

const submit = () => {
    if (!formRef.value) return

    formRef.value.validate((valid, fields) => {
        if (valid) {
            console.log('valid!')
        } else {
            console.log('error', fields)
        }
    })
}

const clear = () => {
  form.functionName = ''
  form.request = ''
}

const response = ref('')

const dialogVisible = ref(false)
</script>
<style scoped>
.card_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
