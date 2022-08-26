<template>
  <div class="loginblock">
    <h2>
      AIserver
      <div class="contain">
        <span>AIserver</span>
        <span>AIserver</span>
      </div>
      <div class="contain">
        <span>AIserver</span>
        <span>AIserver</span>
      </div>
      <div class="center" v-if="islogin===1">
        <form onsubmit="return false">
          <label>登录界面</label><br/>
          <label>用户名: </label>
          <input type='text' name = 'user' placeholder="请输入您的用户名" required v-model="username"/><br/>
          <label>密  码: </label>
          <input type='password' autocomplete="off" name = 'password' placeholder="请输入您的密码" required v-model="password"/><br/>
          <button type="button" @click="changelogin(0)"><span>注册</span></button>
          <button type="submit" @click="updataall"><span>登录</span></button>
        </form>
      </div>
      <div class="center" v-else>
        <form onsubmit="return false">
          <label>注册界面</label><br/>
          <label>用户名: </label>
          <input type='text' name = 'user' placeholder="请输入您的用户名" required v-model="username"/><br/>
          <label>密  码: </label>
          <input type='password' autocomplete="off" name = 'password' placeholder="请输入您的密码" required v-model="password"/><br/>
          <button type="button" @click="changelogin(1)"><span>返回</span></button>
          <button type="submit" @click="reg"><span>注册</span></button>
        </form>
      </div>
    </h2>   
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useStore } from 'vuex'
import axios from "axios";

export default defineComponent({
  name: 'login',
  components: {
  },
  data () {
    return {
      username:'',
      password:'',
      store: useStore(),
      islogin:1,
    }
  },
  methods: {
    changelogin(index:number){
      this.islogin = index;
    },
    reg(){
      if(this.username!=''&& this.password!=''){
        let param = new FormData();
        param.append('user',this.username);
        param.append('password',this.password);
        var path = 'http://127.0.0.1:5000/register';
        axios.post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
          .then((response: any)=> {
            if (response.data.status === 'success') {
              this.islogin = 1;
            } else if (response.data.status === 'duplication') {
              alert("用户已经存在！请换一个名字！");
            }
          });
      }
      else{
        alert("请不要输入空的用户名！")
      }
    },
    updataall(){
      if(this.username!=''&& this.password!=''){
        let param = new FormData();
        param.append('user',this.username);
        param.append('password',this.password);
        var path = 'http://127.0.0.1:5000/login';
        axios.post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
          .then((response: any)=>{
          if (response.data.status === 'success'){
            this.store.commit('saveusername',this.username);
            this.store.commit('savepassword',this.password);
            this.$router.push('/model_manage')
          }
          else if(response.data.status === 'user not found'){
            alert("用户不存在！请先注册！")
          }
          else if(response.data.status === 'invalid password'){
            alert("密码错误！")
          }
        });
      }
    },
  },
});
</script>

<style scoped>
.loginblock{
  margin:0;
  padding: 0;
  min-height: 90vh;
  font-family: consolas;
  background: linear-gradient(to right, white 0%, white 50%, black 50%, black 100%);
  
}

h2{
  position: absolute;
  top: 50%;
  left: 50%;
  height: 400px;
  transform: translate(-50%,-50%);
  margin: 0;
  padding: 0;
  font-size:8em;
  color: transparent;
  text-transform: uppercase;
  background: inherit;
}

h2 div[class="contain"]:nth-child(1){
  position: absolute;
  top:31%;
  left:0;
  color: white;
  mix-blend-mode: difference;
  transition: 0.5s;
  clip-path: polygon(0 0,100% 0,100% 50%,2% 50%);
  overflow: hidden;
}

h2:hover div[class="contain"]:nth-child(1){
  transform: translateY(-108px);
}

h2 div[class="contain"]:nth-child(2){
  position: absolute;
  top:31%;
  left:0;
  color:white;
  transition: 0.5s;
  clip-path: polygon(0 50%,100% 50%,100% 100%,0% 100%);
  overflow: hidden;
  mix-blend-mode: difference;
}

h2:hover div[class="contain"]:nth-child(2){
  transform: translateY(120px);
}

h2 div[class="center"]{
  position: absolute;
  display: block;
  height: 200px;
  top:55%;
  left:0;
  transform: translateY(-50%) scaleY(0);
  color:black;
  background: #F1F2F6;
  border: 4px solid rgb(179, 191, 231);
  font-size:20px;
  letter-spacing: 0.7em;
  text-align: center;
  padding-left: 20px;
  margin-left: 120px;
  transition: 0.5s;
  line-height: 40px;
}

h2:hover div[class="center"]{
  transform: translateY(-50%) scaleY(1);
}

h2 div[class="contain"]:nth-child(1) span:nth-child(1){
  color:transparent;
  -webkit-text-stroke: 2px white;
}

h2 div[class="contain"]:nth-child(1) span:nth-child(2){
  color:white;
  position: absolute;
  left:0;
  animation: animate 8s ease-in-out infinite;
}

h2 div[class="contain"]:nth-child(2) span:nth-child(1){
  color:transparent;
  -webkit-text-stroke: 2px white;
}

h2 div[class="contain"]:nth-child(2) span:nth-child(2){
  color: white;
  position: absolute;
  left:0;
  animation: animate 8s ease-in-out infinite;
}

@keyframes animate {
  0% , 100%{
    clip-path: polygon(0% 50%, 18% 60%, 35% 56%, 50% 51%, 67% 57%, 83% 55%, 100% 45%, 100% 100%, 0 100%);
  }

  25%, 75% {
    clip-path: polygon(0 57%, 17% 69%, 36% 66%, 53% 60%, 69% 65%, 86% 61%, 100% 51%, 100% 100%, 0 100%);
  }

  50%{
    clip-path: polygon(0 74%, 22% 70%, 40% 82%, 62% 81%, 78% 70%, 90% 78%, 100% 90%, 100% 100%, 0 100%);
  }
}

form{
  display: block;
  margin: 10px 20px;
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