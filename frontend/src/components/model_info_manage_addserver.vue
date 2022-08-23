<template>
  <div class="context">
    <div class="addserverblock">
      <span class="totaltitle"><label class="totalname">部署服务信息填写</label></span>
      <span style="white-space:pre"></span><span class="line"></span>
      <form onsubmit="return false">
        <label class='servername' >部署服务名称</label>
        <input type="text" v-model="name" />
        <!-- <label class='servername' >类型</label>
        <input type="text" v-model="webtype"/>
        <label class='servername'>开始时间</label>
        <input type="text" v-model="starttime"/>
        <label class='servername'>状态</label>
        <input type="text" v-model="state"/>
        <label class='servername'>操作</label>
        <input type="text" v-model="operator"/> -->
        <div class="buttonspace">
          <button type="button" @click="pagechange(3)"><span>返回</span></button>
          <button type="submit" @click="uploaddata()"><span>确认</span></button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'model_info_addserver',
  props: {
    msg: String,
  },
  data(){
    return {
      store: useStore(),
      name:'',
      // webtype:'',
      // starttime:'',
      // state:'',
      // operator:'',
    }
  },
  methods:{
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
    //小于10的拼接上0字符串
    addZero(s:number) {
        return s < 10 ? ('0' + s) : s;
    },
    pagechange(index:number){
        this.$emit('pagechange',index);
    },
    uploaddata(){
        // if(this.name!='' &&
        // this.webtype!='' &&
        // this.starttime!='' &&
        // this.state!='' &&
        // this.operator!='' ){
        if(this.name!=''){
          let param=new FormData();
          param.append('user',this.store.state.username);
          param.append('password',this.store.state.password);
          param.append('modelname',this.store.state.modelname);
          param.append('deployment',this.name);
          param.append('time',this.getvalue())
          var path1 = 'http://127.0.0.1:5000/createdeployment';
          axios
            .post(path1,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
            .then(res=> {
              if(res.data.status==='success'){
                this.store.commit('savewebname',this.name);
                this.store.commit('savecorrecttime',this.getvalue());
                this.$router.push('/deploy')
              }
              else{
                if(res.data.status==='duplication'){
                  alert("部署名重复");
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
              });
            var path2 = 'http://127.0.0.1:5000/setdeploymentstatusrunning';
            axios
            .post(path2,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
            .then(res=> {
                if(res.data.status==='deployment not found'){
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
        }
    },
  }
});
</script>

<style scoped>
.context {
    height: 500px;
    width: auto;
    background: #F1F2F6;
}

.addserverblock {
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
span[class='totaltitle']{
  display: inline-block;
  width: 100%;
  text-align: center;
}
label[class='totalname'] {
  font-weight: bold;
  font-size: 30px;
}
.line {
  display: inline-block;
  padding-top : 3px;
  width: 100%;
  border-top: 1px solid #666666;
}
label[class='servername']{
  left:10px;
  font-size: 20px;
  font-weight: lighter;
}
form{
  display: block;
  margin: 20px 50px;
}

input {
  font-size: 20px;
  width: 100%;
  margin-top: 10px;
}

.buttonspace{
  display: flex;
  margin: 30px 0px;
}

button{
  flex:1;
  position: relative;
  top:8px;
  border: none;
  display: inline-block;
  padding: 10px 30px;

  margin: 0px 20px;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 2px;
  color:#5a94a2;
  border-radius: 40px;
  box-shadow: -2px -2px 8px rgba(255, 255, 255, 1),-2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),2px 2px 8px rgba(0, 0, 0, 0.15);
}

button:hover{
  box-shadow: inset -2px -2px 8px rgba(255, 255, 255, 1),inset -2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),inset 2px 2px 8px rgba(0, 0, 0, 0.15);
}

button:hover:span{
  display: inline-block;
  transform: scale(0.98);
}
</style>
