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
            <el-input
              type="textarea"
              :rows="4"
              v-model="form.preparationCode"
            ></el-input>
          </el-form-item>
          <span style="text-align: left">请求内容</span>
          <el-radio-group v-model="requestChoice" class="ml-4">
            <el-radio label="JSON" size="small">JSON参数</el-radio>
            <el-radio label="File" size="small">文件</el-radio>
          </el-radio-group>
          <el-form-item v-show="requestChoice == 'JSON'" prop="requestJSON">
            <el-input
              type="textarea"
              :rows="4"
              v-model="form.requestJSON"
            ></el-input>
          </el-form-item>
          <el-form-item v-show="requestChoice == 'File'" prop="requestFile">
            <input type="file" @change="getFile" id="fileInput" ref="input" />
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
  ElInput,
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
  preparationCode: "import json \nimport os \nimport prepare as default_prepare \ndef prepare(input_type, file): \nif isinstance(file, str): \n# 如果您传入的是字符串可以直接使用json.loads \nreturn json.loads(file) \nelse: \nfilepath = './input_file/' + file.filename \nfile.save(filepath) \ndata = None \n# todo # 如果您传入的是jpg \n# data = default_prepare.readimg(input_type[0], filepath, file) \n# 如果您传入的是mp4 \n# data = default_prepare.readmp4(input_type[0], filepath, file) \n# 如果您传入的是txt \n# data = default_prepare.readtxt(input_type, filepath, file)  \n# 如果您传入的是csv \n# data = default_prepare.readcsv(input_type, filepath, file) \n# 如果您传入的是zip \n# data = default_prepare.readzip(input_type, filepath, file) \nos.remove(filepath) \nreturn data",
  requestJSON: '',
  requestFile: null,
})
type RequestChoice = 'JSON' | 'File'

const requestChoice = ref<RequestChoice>('JSON')
const formRef = ref<FormInstance>()
const store = useStore()

const input = ref()

const getFile = () => {
  //获取file内容
  console.log('getFile', input.value)
  if (input.value) {
    form.requestFile = input.value.files[0]
    //this.filename = this.file.name;
    console.log(form.requestFile)
  }
}

const submit = () => {
  if (form.requestJSON.length == 0 && form.requestFile == null) {
    alert('未提交请求！')
    return
  }
  const path = `http://127.0.0.1:5000/testmodel_quickresponse/${store.state.webname}`
  const param = new FormData()
  param.append('file', form.requestJSON || form.requestFile || '')
  param.append('prepare_py', form.preparationCode)
  request(path, param).then((res: any) => {
    if (res.data.status == 'success') {
      console.log(response)
      response = res.data.output
      console.log(response)
    } else if (res.data.status == 'runtime error') {
      alert('运行时错误')
    } else if (res.data.status == 'model not found') {
      alert('模型不存在')
    } else if (res.data.status == 'preprocess failed') {
      alert('预处理失败，请检查语法')
    } else {
      alert(res.data.status)
    }
  })
}

const clear = () => {
  form.preparationCode = ''
  form.requestJSON = ''
  form.requestFile = null
}

var response = '{"a": 1}'

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
  flex-grow: 1;
  display: block;
  margin: 20px;

  overflow: auto;
  background: white;
  text-align: left;
  border: 4px solid rgb(179, 191, 231);
  border-radius: 10px;
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
