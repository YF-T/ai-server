<!--<template>-->
<!--<div class= "body">-->
<!--<div class = "face">-->
<!--  <div class="eyes">-->
<!--    <div class="eye"></div>-->
<!--    <div class="eye"></div>-->
<!--  </div>-->
<!--</div>-->
<!--</div>-->
<!--</template>-->

<!--<script>-->
<!--import { defineComponent } from 'vue';-->
<!--document.querySelector(".body").addEventListener('mousemove',-->
<!--eyeball)-->
<!--function eyeball(){-->
<!--  let eyes = document.querySelectorAll('.eye');-->
<!--  eyes.forEach(eye=>{-->
<!--    let x = (eye.getBoundingClientRect().left)+(eye.clientWidth/2)-->
<!--    let y = (eye.getBoundingClientRect().top)+(eye.clientHeight/2)-->
<!--    let radian = Math.atan2(event.pageX - x,event.pageY -y)-->
<!--    let rot = (radian * (180/Math.PI) * -1) +270-->
<!--    eye.style.transform = `rotate(${rot}deg)`-->
<!--  })-->
<!--}-->
<!--export default defineComponent({-->
<!--  name:"face",-->
<!--  components:{},-->
<!--  data(){-->
<!--    return{-->
<!--    }-->
<!--  },-->

<!--});-->
<!--</script>-->

<!--<style scoped>-->
<!--*{-->
<!--  margin: 0;-->
<!--  padding: 0;-->
<!--  box-sizing:border-box;-->
<!--}-->
<!--.body{-->
<!--  display: flex;-->
<!--  justify-content: center;-->
<!--  align-items: center;-->
<!--  min-height: 100vh;-->
<!--  background: lightpink;-->
<!--}-->

<!--.face{-->
<!--  position:relative;-->
<!--  width:300px;-->
<!--  height:300px;-->
<!--  border-radius: 50%;-->
<!--  background:grey;-->
<!--  display:flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--}-->

<!--.face:before{-->
<!--  content: '';-->
<!--  position: absolute;-->
<!--  top:180px;-->
<!--  width:150px;-->
<!--  height:70px;-->
<!--  background:lightgrey;-->
<!--  border-bottom-left-radius: 70px;-->
<!--  border-bottom-right-radius: 70px;-->
<!--  transition: 0.5s;-->
<!--}-->

<!--.face:hover:before{-->
<!--  top:210px;-->
<!--  width:150px;-->
<!--  height:20px;-->
<!--  background:lightgrey;-->
<!--  border-bottom-left-radius: 0;-->
<!--  border-bottom-right-radius: 0;-->
<!--}-->

<!--.eyes{-->
<!--  position: relative;-->
<!--  top:-40px;-->
<!--  display: flex;-->
<!--}-->

<!--.eyes .eye{-->
<!--  position: relative;-->
<!--  width:80px;-->
<!--  height:80px;-->
<!--  display: block;-->
<!--  background: #ffffff;-->
<!--  margin: 0 15px;-->
<!--  border-radius: 50%;-->
<!--}-->

<!--.eyes .eye::before{-->
<!--  content: '';-->
<!--  position: absolute;-->
<!--  top:50%;-->
<!--  left:25px;-->
<!--  transform: translate(-50%, -50%);-->
<!--  width: 40px;-->
<!--  height:40px;-->
<!--  background: #333;-->
<!--  border-radius: 50%;-->
<!--}-->
<!--</style>-->