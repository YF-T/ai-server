<template>
  <div>
    <div class="model_info_show">
      <table>
        <tr>
          <th width = "40%">任务名称</th>
          <th width = "20%">修改时间</th>
          <th width = "10%">类型</th>
          <th width = "20%">算法</th>
          <th width = "10%">引擎</th>
        </tr>
        <tr>
          <td>{{modelname}}</td>
          <td>{{modification_time}}</td>
          <td>{{modeltype}}</td>
          <td>{{algorithm}}</td>
          <td>{{engine}}</td>
        </tr>
      </table>      
    </div>

    <nav>
      <ul class="item">
        <li><a @click="show(1)" :class="index===1? 'active':'no'">概述</a></li>
        <li><a @click="show(2)" :class="index===2? 'active':'no'">测试</a></li>
        <li><a @click="show(3)" :class="index===3 || index===4? 'active':'no'">部署</a></li>
		  </ul>
    </nav>
    <!-- 面板一 -->
    <model_info_overview v-show="index===1"/>
    <!-- 面板二 -->
    <model_info_test @pagechange="mainpagechange" v-show="index===2"/>
    <!-- 面板三 -->
    <model_info_deploy @pagechange="mainpagechange" v-show="index===3" :key="index===3?1:2"/>
    <!-- 面板四 -->
    <model_info_addserver @pagechange="mainpagechange" v-show="index===4"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import model_info_overview from '@/components/model_info_manage_overview.vue'; 
import model_info_test from '@/components/model_info_manage_test.vue'; 
import model_info_deploy from '@/components/model_info_manage_deploy.vue'; 
import model_info_addserver from  '@/components/model_info_manage_addserver.vue'; 
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  name: 'model_info_manage',
  components: {
    model_info_overview,
    model_info_test,
    model_info_deploy,
    model_info_addserver,
  },
  created:function(){
    this.modelinfoshow();
  },
  data () {
    return {
      index: 1,
      modelname:'未知',
      modification_time:'未知',
      modeltype:'未知',
      algorithm:'未知',
      engine:"未知",
      store: useStore(),
    }
  },
  methods: {
    show (value: number) {
      this.index = value;
    },
    mainpagechange(value:number){
      this.index = value;
    },
    modelinfoshow(){
      let param=new FormData();
      console.log(this.store.state.username,this.store.state.password,this.store.state.modelname)
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      var path = 'http://127.0.0.1:5000/getmodelinfo';
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
        .then((res: any) => {
          console.log(res.data.status);
          if(res.data.status==='success'){
            this.modelname = res.data.modelname;
            this.modification_time = res.data.time;
            this.modeltype = res.data.modeltype;
            this.algorithm = res.data.algorithm;
            this.engine = res.data.engine;
          }
        });
    },
  },
});
</script>

<style scoped>
.model_info_show {
  height: 100px;
  background: white;
}

.model_info_show table{
  width: 100%;
  height: 100px;
}

nav{
	width: 100%;
	height: 100px;
	background-color: black;
}

.item{
	position:sticky;/*固定在页面顶部*/
  width: 100%;
  height: 100px;
	margin: 0;
	padding: 0;
	display: flex;/*弹性布局，使li排成一行*/
}
.item li{
	list-style: none;
  /* height: 100px; */
  flex-grow: 1;
}
.item li a{
	position: relative;
	display: block;
  height: 100px;
  line-height: 100px;
	color: white;
	font-weight: bold;
}

.item li a[class="active"]{
  background:white;
  color:black;
  
}

.item li a[class="no"]:hover{
	color:black;
}

.item li a[class="no"]:after{
	content:'';
	position: absolute;
	left: 0;
	width: 100%;
	height: 100%;
	background: white;
	transform: scale(0);
	transition: 0.5s;
	z-index: -1;
}
.item li a[class="no"]:hover:after{
	transform: scale(1);
}
</style>


