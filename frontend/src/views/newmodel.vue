<template>
<div id="all">
  <div id="name">
  <label class="mname">名称:</label><input type='text' v-model="modelname" />
  </div>
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
  <button @click="importance">导入</button>
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
   },
    importance(){
      let param = new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modeltype',this.modeltype);
      param.append('file',this.file);//TODO
      param.append('time',current);
      param.append('description',this.op);
      var path = 'http://127.0.0.1:5000/upload';
      
      axios.post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
          .then(response=>{console.log(response.data);});
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
div{
  outline:medium solid gold;
}
#all{
  outline:none;
  height:570px;
  line-height: 570px;
}
#name{
  background-image: linear-gradient( 135deg, black 10%, white 100%);
  width:250px;
  height:200px;
  line-height:200px;
  position:absolute;
  left:300px;
  top:150px;
}

#type{
  background-image: linear-gradient( 225deg, black 10%, white 100%);
  width:250px;
  height:200px;
  line-height:200px;
  position:absolute;
  right:300px;
  top:150px;
}

#myfile{
  background-image: linear-gradient( 0deg, black 10%, white 100%);
  width:250px;
  height:200px;
  line-height:200px;
  position:absolute;
  right:645px;
  bottom:50px;
}
.mname{
  display:inline-block;
  font-size: large;
  color:snow;
}

#inputfile{
  font-size: large;
  margin-left: 40px;
}

button{
    width: 120px;
    height: 120px;
    border-radius:50%;
    background-color: skyblue;
    border: 10px solid lightslategrey;
    display:inline-block;
}

</style>