<template>
<div>
  <div id="main">
  <div></div>
  <div id="name">
  <label class="mname">名称:</label><input type='text' v-model="modelname" />
  </div>
  <div></div>
  <div></div>
  <div id = "button" class="mname" @click="importance">导入</div>
  <div id="type">
  <label class="mname">类型: </label>
  <select v-model="modeltype">
    <option value ="pmml">pmml</option>
    <option value ="onnx">onnx</option>
  </select>
  </div>
  <div id="myfile">
    <input id="inputfile" type="file" ref="fileId" @change="getFile">
  </div>
  <div></div>
  <div></div>
  </div>
  <div class="back" @click="back">返回</div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex'
import axios from "axios"

let now = new Date()
let m = now.getMinutes()
let s = now.getSeconds()
let current = now.getHours()+':'+ (m < 10 ?  '0'  + m: m) +':'+ (s < 10 ?  '0'  + s: s)

export default defineComponent({
  name: "newmodel",
  components:{},
  data(){
    return{
      store:useStore(),
      modelname:'',
      modeltype:'pmml',
      time:current,
      op:"???",
      file:''
    }
  },
  methods:{
    getFile(){
     //获取file内容
    let files:any = this.$refs.fileId;
    this.file = files.files[0];
    //this.filename = this.file.name;
    console.log(files.files);
    console.log(this.file);

   },
    back(){
      this.$router.push('/model_manage');
    },
    importance(){
      let param = new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modeltype',this.modeltype);
      param.append('file',this.file);
      param.append('time',current);
      param.append('description',this.op);
      var path = 'http://127.0.0.1:5000/upload';
      axios.post(path,param)
          .then(response=>{
            console.log(response.data);
            if (response.data.status === false)
            {
              alert("对不起，您的模型上传失败了！");
            }
          });

      let data = {
        modelname:this.modelname,
        modeltype:this.modeltype,
        time:this.time,
        op:"???"
      }
      this.store.commit('savemodelname',this.modelname);
      this.store.commit('savedetail',data);
      this.$router.push('/model_info_manage');
    }
  }

});
</script>

<style scoped>
#main{
  display:grid;
  grid-template-rows:33% 33% 34%;
  grid-template-columns:33% 33% 34%;
}

#main div{
  background-image: radial-gradient(black,grey);
  height:200px;
  line-height:200px;
  font-size: xx-large;
  border: grey thick solid;

}

#main div:hover{
  border: skyblue thick solid;
  background-image: radial-gradient(white,grey);
  transition: background-image 1s;
}

#main div:active{
  background-image: linear-gradient(white,lightpink);
}

.mname{
  display:inline-block;
  font-size: xx-large;
  color:gold;
}

#inputfile{
  font-size: xx-large;
  margin-left: 80px;
  color:gold;
}

select{
  width:70px;
  height:25px;
}

.back{
  height:53px;
  font-size: xx-large;
  color:gold;
  background-image: radial-gradient(black,grey)
}
</style>