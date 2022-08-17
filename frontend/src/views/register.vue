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
        <input type="submit" value = "注册" @click="reg"/>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from "axios";

export default defineComponent({
  name: "register",
  components: {
  },
  data () {
    return {
      username:'',
      password:''
    }
  },
  methods:{
    reg(){
      if(this.username!=''&& this.password!=''){
        let param = new FormData();
        param.append('user',this.username);
        param.append('password',this.password);
        var path = 'http://127.0.0.1:5000/register';
        axios.post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
          .then(response=> {
            console.log(response);
            if (response.data.status === 'success') {
              this.$router.push('/')
            } else if (response.data.status === 'duplication') {
              alert("用户已经存在！请换一个名字！");
            }
          });
      }
      else{
        alert("请不要输入空的用户名！")
      }
    }
  }
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