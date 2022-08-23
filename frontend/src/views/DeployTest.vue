<template>
  <div>
    <div class="cards">
      <el-card style="card" class="card" shadow="never">
        <template #header>
          <div class="card_header">
            <span>请求</span>
            <el-link type="primary" @click="openDialog">生成代码</el-link>
          </div>
        </template>
        <el-form :model="form" label-position="top" ref="formRef" class="form">
          <el-form-item label="Python 预处理代码" prop="preparationCode">
            <CodeEditor
              language="python"
              :width="800"
              :height="300"
              :value="form.preparationCode"
              @update:value="handleUpdate('preparationCode')"
            />
          </el-form-item>
          <span style="text-align: left">请求内容</span>
          <el-radio-group v-model="requestChoice" class="ml-4">
            <el-radio label="JSON" size="small">JSON参数</el-radio>
            <el-radio label="File" size="small">文件</el-radio>
          </el-radio-group>
          <el-form-item v-if="requestChoice == 'JSON'" prop="requestJSON">
            <CodeEditor
              language="javascript"
              :width="800"
              :height="300"
              :value="form.requestJSON"
              @update:value="handleUpdate('requestJSON')"
            />
          </el-form-item>
          <el-form-item v-else="requestChoice == 'File'" prop="requestFile">
            <input type="file" @change="chooseUploadFile" id="fileInput" />
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

    <el-dialog v-model="dialogVisible" title="生成 CURL 代码">
      <div class="dialog">
        <CodeViewer :code="curlCode" language="shell"></CodeViewer>
        <small>代码已复制到剪贴板</small>
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
      </div>
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import {
  ElCard,
  ElLink,
  ElForm,
  ElFormItem,
  ElButton,
  ElButtonGroup,
  ElRadio,
  ElRadioGroup,
  ElDialog,
} from 'element-plus'
import { reactive, ref, onMounted } from 'vue'
import type { FormRules, FormInstance } from 'element-plus'
import CodeViewer from '../components/CodeViewer.vue'
import CodeEditor from '../components/CodeEditor.vue'
import { request } from '../Util'
import { useStore } from 'vuex'

const form = reactive({
  preparationCode: '',
  requestJSON: '',
  requestFile: null,
})
type RequestChoice = 'JSON' | 'File'

const requestChoice = ref<RequestChoice>('JSON')
const formRef = ref<FormInstance>()
const store = useStore()

const chooseUploadFile = (e: any) => {
  const file = e.target.files.item(0).getAsFile()
  if (!file) return
  form.requestFile = file
  // 清空，防止上传后再上传没有反应
  e.target.value = ''
}

const submit = () => {
  if (form.requestJSON.length == 0 || form.requestFile == null) {
    alert('未提交请求！')
    return
  }
  const path = `http://127.0.0.1:5000/testmodel_quickresponse/${store.state.webname}`
  const param = new FormData()
  param.append('file', form.requestJSON || form.requestFile || '')
  param.append('prepare_py', form.preparationCode)
  request(path, param).then((res: any) => {
    if (res.status == 'success') {
      response.value = res.output
    } else if (res.status == 'runtime error') {
      alert('运行时错误')
    } else if (res.status == 'model not found') {
      alert('模型不存在')
    } else if (res.status == 'preprocess failed') {
      alert('预处理失败，请检查语法')
    }
  })
  
}

const clear = () => {
  form.preparationCode = ''
  form.requestJSON = ''
  form.requestFile = null
}

const response = ref('{"a": 1}')

const dialogVisible = ref(false)

const endpoint = ref('https://ddddd')

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text)
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

const curlCode = `curl -k -X '${endpointType.value}' \\
${endpoint.value} \\
-H 'Cache-Control: no-cache' \\
-H 'Content-Type: application/json' \\
-d ${form.requestJSON}`

const handleUpdate = (key: keyof typeof form) => (value: string) => {
  form[key] = value
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
    flex-grow:1;
  display:block;
  margin: 20px;
  height: 400px;
  overflow: auto;
  background: white;
  text-align:left;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
}

.el-table thead {
  --el-table-header-text-color: black;
}

.form {
  display: flex;
  flex-direction: column;
  flex-gap: 10px;
}

.dialog {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
}
</style>
