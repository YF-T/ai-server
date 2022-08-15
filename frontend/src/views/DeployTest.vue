<template>
  <div>
    <div class="details">
      <div>
        <span class="caption">端点:</span><el-tag>{{ endpointType }}</el-tag
        ><span class="endpoint">{{ endpoint }}</span>
      </div>
      <div>
        <span class="caption">部署令牌: </span
        ><el-icon color="#e32461" @click="copyToken" class="copy_token"
          ><CopyDocument
        /></el-icon>
      </div>
    </div>
    <div class="cards">
      <el-card style="card" class="card" shadow="never">
        <template #header>
          <div class="card_header">
            <span>请求</span>
            <el-link type="primary" @click="openDialog">生成代码</el-link>
          </div>
        </template>
        <el-form
          :model="form"
          label-position="top"
          :rules="rules"
          ref="formRef"
        >
          <el-form-item label="函数名" prop="functionName">
            <el-input v-model="form.functionName"></el-input>
          </el-form-item>
          <el-form-item label="请求" prop="request">
            <CodeEditor
              language="javascript"
              :width="800"
              :height="400"
              :value="form.request"
              @update:value="handleUpdate"
              :options="{
                minimap: {
                  enabled: false,
                },
              }"
            ></CodeEditor>
          </el-form-item>
          <el-form-item>
            <el-button-group>
              <el-button @click="clear">清除</el-button>
              <el-button @click="submit" type="primary">提交</el-button>
            </el-button-group>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card style="card" class="card" shadow="never">
        <template #header>
          <div class="card_header">
            <span>响应</span>
          </div>
        </template>
        <CodeViewer :code="response" :language="'javascript'" />
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" title="生成代码">
      <small>代码已复制到剪贴板</small>
      <CodeViewer :code="curlCode" language="shell"></CodeViewer>

      <el-button
        type="primary"
        @click="
          () => {
            dialogVisible = false
          }
        "
      >
        关闭
      </el-button>
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
  ElIcon,
} from 'element-plus'
import { CopyDocument } from '@element-plus/icons-vue'
import { reactive, ref, onMounted, nextTick } from 'vue'
import type { FormRules, FormInstance } from 'element-plus'
import CodeViewer from '../components/CodeViewer.vue'
import CodeEditor from '../components/CodeEditor.vue'

const handleClick = () => {}
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

const response = ref('{"a": 1}')

const dialogVisible = ref(false)

const endpoint = ref('https://ddddd')

const token = 'token'

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(token)
}
const copyToken = () => {
  copyToClipboard(token)
  alert('copied')
}

const responseEditorRef = ref()
onMounted(() => {
  console.log(responseEditorRef)
  if (responseEditorRef.value) {
    const responseEditor = responseEditorRef.value.editor
    console.log(responseEditor)
    const messageContribution = responseEditor.getContribution(
      'editor.contrib.messageController'
    )
    responseEditor.onDidAttemptReadOnlyEdit(() => {
      messageContribution.closeMessage()
    })
  }
})

const openDialog = () => {
  dialogVisible.value = true
  copyToClipboard(curlCode)
  console.log(dialogVisible.value)
}

const endpointType = ref('POST')

const curlCode = `curl -k -X '${endpointType.value}' \
${endpoint.value} \
-H 'Authorization: Bearer ${token}' \
-H 'Cache-Control: no-cache' \
-H 'Content-Type: application/json' \
-d ${form.request}`

const handleUpdate = (value: string) => {
  form.request = value
}
</script>
<style scoped>
.card_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.endpoint {
  margin-left: 0.5em;
}

.caption {
  margin-right: 0.5em;
}

.copy_token {
  cursor: pointer;
}

.cards {
  display: flex;
}

.details {
  text-align: left;
}
.card {
  width: 50%;
  margin: 0.5em;
}
</style>
