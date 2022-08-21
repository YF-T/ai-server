<template>
<div>
  <h1 id="title">模型管理</h1>
  <label>模型类型 : </label><input type='text' v-model="filter"/>
  <br/><br/>
  <div class="body">
  <div class = "center">
    <div id="thead" v-for="th in title">{{th}} </div>
  </div>
  <br/>
  <div class = "center" v-for = "item in data" v-show = "show(item.modelname)">
<!--  <div class = "center" v-for = "item in this.store.state.details" v-show = "show(item.modeltype)">-->
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
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
          .then(response => {
            console.log(response.data);
            this.data = response.data.model;
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
  background-image: linear-gradient( 135deg, skyblue 10%, violet 100%);
}
#thead{
  float:left;
  text-align:center;
  width:100px;
}
.center{
  width:400px;
  /*position:absolute;*/
  margin-left:570px;
  margin-bottom: 10px;
  margin-top: 10px;
}
.body{
  height:400px;
  overflow-y: scroll;
}

</style>