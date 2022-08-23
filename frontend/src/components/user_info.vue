<template>
  <div class="user_info_show">
    <button v-show="$route.path!='/'&&$route.path!='/newmodel'" @click="changeroute">返回上一个页面</button>
    <div class="contain">
      <span>AI-server</span>
      <span>AI-server</span>
    </div>
    <!-- <h1>{{ msg }}</h1> -->
    <label>用户名：{{store.state.username}}</label>
    <input type="button" @click="colorchange()" :value="ifday===1?'点击开启阴间模式':'点击开启阳间模式'"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex'

export default defineComponent({
  name: 'user_info',
  props: {
    msg: String,
  },
  data() {
    return {
      ifday: 1,
      store: useStore(),
    }
  },
  methods:{
    changeroute(){
      if(this.$route.path == "/model_info_manage")
        this.$router.push('/model_manage')
      else if(this.$route.path == "/model_manage")
        this.$router.push("/")
      else
        this.$router.push("/model_info_manage")
    },
    colorchange(){
      this.ifday = -this.ifday;
      this.$emit("colorchange",this.ifday);
    }
  },
});
</script>

<style scoped>
.user_info_show {
  height: 60px;
  width: auto;
  background: black;
  color: white;
  line-height: 60px;
  display: flex;
  text-align: center;
}

button{
  flex:1;
  border-radius: 7px;
}
.contain{
  flex: 1;
}

.contain span{
  position: absolute;
  color:white;
  font-size: 2em;
}

.contain span:nth-child(1){
  color:transparent;
  -webkit-text-stroke: 2px blue;
}

.contain span:nth-child(2){
  color:blue;
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

label {
  flex:1;
}

input[type='button'] {
  flex:1;
  border-radius: 7px;
}
</style>
