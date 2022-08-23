<template>
<div>
  <h1 id="title">模型管理</h1>
  <label>模型名称 : </label><input type='text' v-model="filter"/>
  <br/><br/>
  <div class="body">
  <div class = "center">
    <div id="thead" v-for="th in title">{{th}} </div>
  </div>
  <br/>
  <div class = "center" v-for = "item in data" v-show = "show(item.modelname)">
<!--  <div class = "center" v-for = "item in this.store.state.details" v-show = "show(item.modelname)">-->
      <model_manage_item :modelname="item.modelname" :modeltype="item.modeltype" :time="item.time" :op="`???`"></model_manage_item>
  </div>
  </div>
  <br/>
  <br/>
  <button @click = "lead">导入模型</button>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import model_manage_item from "@/components/model_manage_item.vue";
import { useStore } from 'vuex'
import axios from "axios";

// 模型管理页面
export default defineComponent({
  name: "model_manage",
  components: {model_manage_item},
  data(){
    return{
      filter:'',
      store: useStore(),
      title:['名称','类型','更新时间','操作'],
      data:[],
    }
  },
  methods:{
    lead(){
      this.$router.push('/newmodel')
    },
    show(name:string){
      if (this.filter == '')
          return true
      return name == this.filter
    },
    showdata() {
      let param = new FormData();
      param.append('user', this.store.state.username);
      param.append('password', this.store.state.password);
      var path = 'http://127.0.0.1:5000/getusermodel ';
      axios.post(path, param)
          .then(response => {
            console.log(response);
            this.data = response.data.model
          });
    }
    },
    mounted() {
      this.showdata();
    }
});
</script>

<style scoped>
button{
  align-content: center;
  margin-bottom: 20px;
  height:80px;
  width:120px;
  font-size: 20px;
  background-color: white;
  border: 3px solid black;
}
#thead{
  float:left;
  text-align:center;
  width:200px;
  border:solid black thin;
}
.center{
  width:810px;
  /*position:absolute;*/
  margin-bottom: 10px;
  margin-top: 10px;
}
.body{
  height:400px;
  width:830px;
  overflow-y: auto;
  margin:auto;
}

</style>