<template>
    <div class="context">
      <div class="deployblock">
          <div class="infoline">
            <label>部署</label>
            <button class="add" @click="pagechange(4)"><span>添加服务</span></button>
          </div>
          <span style="white-space:pre"></span><span class="line"></span>
          <table>
            <tr>
              <th>名称</th>
              <th>开始时间</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
            <tr v-if="store.state.count===0">
              <td>名称</td>
              <td>开始时间</td>
              <td>状态</td>
              <td>操作</td>
            </tr>
            <tr v-else v-for="item in weblist" :key="item" class="itemone">
              <td @click="transdata(item.deployment)">{{item.deployment}}</td>
              <td @click="transdata(item.deployment)">{{item.time}}</td>
              <td @click="transdata(item.deployment)">{{item.status}}</td>
              <td>
                <button class="oper" v-if="item.status==='running'" @click="stopweb(item.deployment)"><span>暂停</span></button>
                <button class="oper" v-else @click="startweb(item.deployment)"><span>启动</span></button>
                <button class="oper" @click="deleteweb(item.deployment)"><span>删除</span></button>
              </td>
            </tr>
          </table>
      </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  name: 'model_info_deploy',
  props: {
    msg: String,
  },
  created(){
    this.infoshow();
  },
  data(){
    return{
      store: useStore(),
      weblist:[],
    }
  },
  methods:{
    deleteweb(){

    },
    getvalue(){
      var date = new Date();
      //年 getFullYear()：四位数字返回年份
      var year = date.getFullYear(); //getFullYear()代替getYear()
      //月 getMonth()：0 ~ 11
      var month = date.getMonth() + 1;
      //日 getDate()：(1 ~ 31)
      var day = date.getDate();
      //时 getHours()：(0 ~ 23)
      var hour = date.getHours();
      //分 getMinutes()： (0 ~ 59)
      var minute = date.getMinutes();
      //秒 getSeconds()：(0 ~ 59)
      var second = date.getSeconds();

      var time = year + '-' + this.addZero(month) + '-' + this.addZero(day) + ' ' + this.addZero(hour) + ':' + this.addZero(minute) + ':' + this.addZero(second);
      return time;
    },
    addZero(s:number) {
        return s < 10 ? ('0' + s) : s;
    },
    startweb(name:string){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      param.append('deployment',name);
      var path = 'http://127.0.0.1:5000/setdeploymentstatusrunning';
      axios
      .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
      .then(res=> {
          if(res.data.status === 'success'){
            this.infoshow();
          }
          else if(res.data.status==='deployment not found'){
            alert("部署不存在");
          }
          else{
            if(res.data.status==="user not found"){
              alert("用户不存在");
            }
            else if(res.data.status === 'invalid password'){
              alert("密码错误！")
            }
          }
        }
        );
    },
    stopweb(name:string){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      param.append('deployment',name);
      var path = 'http://127.0.0.1:5000/setdeploymentstatuspause';
      axios
      .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
      .then(res=> {
          if(res.data.status === 'success'){
            this.infoshow();
          }
          else if(res.data.status==='deployment not found'){
            alert("部署不存在");
          }
          else{
            if(res.data.status==="user not found"){
              alert("用户不存在");
            }
            else if(res.data.status === 'invalid password'){
              alert("密码错误！")
            }
          }
        }
        );
    },
    transdata(name:string){
      this.store.commit('savewebname',name);
      this.store.commit('savecorrecttime',this.getvalue());
      this.$router.push('/deploy')    
    },
    pagechange(index:number){
      this.$emit('pagechange',index);
    },
    infoshow(){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      var path = 'http://127.0.0.1:5000/getmodeldeployment';
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
        .then(res=> {
          console.log(res.data.status);
          if(res.data.status==='success'){
            this.weblist = res.data.deployment;
          }
          });
    }
  }
});
</script>

<style scoped>
.context {
    height: 500px;
    width: auto;
    background: #F1F2F6;
}

.deployblock {
  position: relative;
  display:block;
  top:20px;
  margin: 0px 20px;
  height: 400px;
  overflow: auto;
  background: white;
  text-align:left;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
}

.line {
  display: inline-block;
  padding-top : 3px;
  width: 100%;
  border-top: 1px solid #666666;
}

table{
  width: 100%;
  background: white;
  text-align: center;
}

table th{
  background: #FAFAFA;
}

.infoline{
  display: flex;
  width: 100%;
}

label {
  position: relative;
  left:10px;
  font-weight: bold;
  font-size: 30px;
  flex:4;
}

button[class='add']{
  flex:1;
  position: relative;
  top:8px;
  border: none;
  display: inline-block;
  padding: 10px 30px;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 2px;
  color:#5a94a2;
  border-radius: 40px;
  box-shadow: -2px -2px 8px rgba(255, 255, 255, 1),-2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),2px 2px 8px rgba(0, 0, 0, 0.15);
}

button[class='add']:hover{
  box-shadow: inset -2px -2px 8px rgba(255, 255, 255, 1),inset -2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),inset 2px 2px 8px rgba(0, 0, 0, 0.15);
}

button[class='add']:hover:span{
  display: inline-block;
  transform: scale(0.98);
}

button[class='oper']{
  width: 40%;
  padding: 8px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
  background-color: white; 
  color: black; 
  border: 2px solid #90EE90;
}

button[class='oper']:hover {
    background-color: #87CEFA;
    color: white;
}

.itemone{
  cursor: pointer;
}
</style>
