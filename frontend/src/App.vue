<template>
   <div :class="ifday===1? 'day' : 'night'">
    <user_info @colorchange="recolor"/>
    <router-view/>
    <footer>
      <span id="title">本网页仅为大作业所用，最终解释权归作者团队所有</span>
      <div class="footer">
        <div class="shape">
          <span style="font-size:20px;font-weight: bold;line-height: 40px;">联系邮箱</span><br/>
          <span style="font-size:16px;font-weight: bold;line-height: 20px;">tanyf20</span><br/>
          <span style="font-size:16px;font-weight: bold;line-height: 20px;">@mails.tsinghua.edu.cn</span>
        </div>
        <div class="shape">
          <span style="font-size:20px;font-weight: bold;line-height: 40px;">联系电话</span><br/>
          <span style="font-size:18px;font-weight: bold;line-height: 50px;">13552750170</span>
        </div>
        <div class="shape">
          <span style="font-size:20px;font-weight: bold;line-height: 40px;">github网址</span><br/>
          <a href="https://github.com/YF-T/ai-server" target="_blank" style="text-decoration: none;"><span style="font-size:18px;font-weight: bold;line-height: 50px;">点击跳转到代码仓库</span></a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import user_info from '@/components/user_info.vue'; // @ is an alias to /src

export default defineComponent({
  name: 'APP',
  components: {
    user_info,
  },
  data () {
    return {
      ifday: 1,
    }
  },
  mounted(){
    this.clickEffect();//调用特效函数
  },
  methods:{
    recolor(value){
      this.ifday = value;
    },
    clickEffect() {
    let balls = [];
    let longPressed = false;
    let longPress;
    let multiplier = 0;
    let width, height;
    let origin;
    let normal;
    let ctx;
    const colours = ["#F73859", "#14FFEC", "#00E0FF", "#FF99FE", "#FAF15D"];
    const canvas = document.createElement("canvas");
    document.body.appendChild(canvas);
    canvas.setAttribute("style", "width: 100%; height: 100%; top: 0; left: 0; z-index: 99999; position: fixed; pointer-events: none;");
    const pointer = document.createElement("span");
    pointer.classList.add("pointer");
    document.body.appendChild(pointer);
   
    if (canvas.getContext && window.addEventListener) {
      ctx = canvas.getContext("2d");
      updateSize();
      window.addEventListener('resize', updateSize, false);
      loop();
      window.addEventListener("mousedown", function(e) {
        pushBalls(randBetween(10, 20), e.clientX, e.clientY);
        document.body.classList.add("is-pressed");
        longPress = setTimeout(function(){
          document.body.classList.add("is-longpress");
          longPressed = true;
        }, 500);
      }, false);
      window.addEventListener("mouseup", function(e) {
        clearInterval(longPress);
        if (longPressed == true) {
          document.body.classList.remove("is-longpress");
          pushBalls(randBetween(50 + Math.ceil(multiplier), 100 + Math.ceil(multiplier)), e.clientX, e.clientY);
          longPressed = false;
        }
        document.body.classList.remove("is-pressed");
      }, false);
      window.addEventListener("mousemove", function(e) {
        let x = e.clientX;
        let y = e.clientY;
        pointer.style.top = y + "px";
        pointer.style.left = x + "px";
      }, false);
    } else {
      console.log("canvas or addEventListener is unsupported!");
    }
   
   
    function updateSize() {
      canvas.width = window.innerWidth * 2;
      canvas.height = window.innerHeight * 2;
      canvas.style.width = window.innerWidth + 'px';
      canvas.style.height = window.innerHeight + 'px';
      ctx.scale(2, 2);
      width = (canvas.width = window.innerWidth);
      height = (canvas.height = window.innerHeight);
      origin = {
        x: width / 2,
        y: height / 2
      };
      normal = {
        x: width / 2,
        y: height / 2
      };
    }
    class Ball {
      constructor(x = origin.x, y = origin.y) {
        this.x = x;
        this.y = y;
        this.angle = Math.PI * 2 * Math.random();
        if (longPressed == true) {
          this.multiplier = randBetween(14 + multiplier, 15 + multiplier);
        } else {
          this.multiplier = randBetween(6, 12);
        }
        this.vx = (this.multiplier + Math.random() * 0.5) * Math.cos(this.angle);
        this.vy = (this.multiplier + Math.random() * 0.5) * Math.sin(this.angle);
        this.r = randBetween(8, 12) + 3 * Math.random();
        this.color = colours[Math.floor(Math.random() * colours.length)];
      }
      update() {
        this.x += this.vx - normal.x;
        this.y += this.vy - normal.y;
        normal.x = -2 / window.innerWidth * Math.sin(this.angle);
        normal.y = -2 / window.innerHeight * Math.cos(this.angle);
        this.r -= 0.3;
        this.vx *= 0.9;
        this.vy *= 0.9;
      }
    }
   
    function pushBalls(count = 1, x = origin.x, y = origin.y) {
      for (let i = 0; i < count; i++) {
        balls.push(new Ball(x, y));
      }
    }
   
    function randBetween(min, max) {
      return Math.floor(Math.random() * max) + min;
    }
   
    function loop() {
      ctx.fillStyle = "rgba(255, 255, 255, 0)";
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < balls.length; i++) {
        let b = balls[i];
        if (b.r < 0) continue;
        ctx.fillStyle = b.color;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2, false);
        ctx.fill();
        b.update();
      }
      if (longPressed == true) {
        multiplier += 0.2;
      } else if (!longPressed && multiplier >= 0) {
        multiplier -= 0.4;
      }
      removeBall();
      requestAnimationFrame(loop);
    }
   
    function removeBall() {
      for (let i = 0; i < balls.length; i++) {
        let b = balls[i];
        if (b.x + b.r < 0 || b.x - b.r > width || b.y + b.r < 0 || b.y - b.r > height || b.r < 0) {
          balls.splice(i, 1);
        }
      }
    }
  }
  },
})
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body{
  margin:0px;
}
.night{
  filter:invert(1);
}

footer{
  height:180px;
  width: 100%;
  text-align: center;
  background: black;
}

.footer{
  height:150px;
  display: flex;
  justify-content: space-around;
  align-items:center;
  width: 100%;
}

.shape {
  width: 200px;
  height: 100px;
  font-size:20px;
  
  color:black;
  background: white;
  position: relative;
  -moz-border-radius:  10px;
  -webkit-border-radius: 10px;
  border-radius:  10px;
}
.shape:before {
   content:"";
   position: absolute;
   right: 100%;
   top: 26px;
   width: 0;
   height: 0;
   border-top: 13px solid transparent;
   border-right: 26px solid white;
   border-bottom: 13px solid transparent;
}

span[id='title']{
  position: relative;
  top:10px;
  font-size: 20px;
  color:white;
  font-weight: bold;
}

a{
  color:black;
}

a:hover{
  color:blue;
}
</style>
