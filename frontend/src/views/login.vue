<template>
  <div class="loginblock">
    <div class="uppart">
      <span></span>
      <span></span>
    </div>
    <div class="downpart">
      <span></span>
      <span></span>
    </div>
    <div class="center">
      <form>
        <label>用户名: </label>
        <input type='text' name = 'user' placeholder="请输入您的用户名" required v-model="username"/><br/><br/>
        <label>密  码: </label>
        <input type='password' name = 'password' placeholder="请输入您的密码" required v-model="password"/><br/><br/>
        <input type="submit" value="登录" @click="updataall"/>
      </form>
      <router-link to="/register">注册</router-link>
    </div>
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
    }
  },
  methods: {
    updataall(){
      if(this.username!=''&& this.password!=''){
        let param = new FormData();
        param.append('user',this.username);
        param.append('password',this.password);
        var path = 'http://127.0.0.1:5000/login';
        axios.post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
          .then(response=>{
          console.log(response);
          if (response.data.status === 'success'){
            this.store.commit('saveusername',this.username);
            this.store.commit('savepassword',this.password);
            this.$router.push('/model_info_manage')
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

  position:relative;
  display: flex;
  height: 300px;
  margin-top: 200px;
  background-image: linear-gradient( 135deg, skyblue 10%, violet 100%);
}
.center{
  margin:auto;
  align-content:center;
}
</style>