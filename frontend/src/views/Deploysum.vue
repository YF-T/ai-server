<template>
  <div>    
    <div class="web_info_show">
      <table>
        <tr>
          <th width = "30%">服务名称</th>
          <th width = "30%">模型对象</th>
          <th width = "20%">修改时间</th>
          <th width = "20%">类别</th>
        </tr>
        <tr>
          <td>{{store.state.webname}}</td>
          <td>{{store.state.modelname}}</td>
          <td>{{store.state.correcttime}}</td>
          <td>网络服务</td>
        </tr>
      </table>      
    </div>
    <nav>
      <ul class="item">
        <li><a @click="show('/deploy/')" :class="$route.path==='/deploy/' || $route.path==='/deploy'? 'active':'no'">概述</a></li>
        <li><a @click="show('/deploy/test')" :class="$route.path==='/deploy/test'? 'active':'no'">快速返回测试</a></li>
        <li><a @click="show('/deploy/tasks')" :class="$route.path==='/deploy/tasks'? 'active':'no'">任务详细信息</a></li>
	  </ul>
    </nav>
    <router-view/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  name: 'Deploysum',
  data(){
    return{
        store: useStore(),
    }
  },
  methods:{
    show(address:string){
        this.$router.push({ path: address });
    }
  }
});
</script>

<style scoped>
.web_info_show {
  height: 100px;
  background: white;
}

.web_info_show table{
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


