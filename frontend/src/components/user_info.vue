<template>
  <div class="user_info_show">
    <div class="contain">
      <!-- <h2>water</h2> -->
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
  -webkit-text-stroke: 2px purple;
}

.contain span:nth-child(2){
  color:purple;
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
