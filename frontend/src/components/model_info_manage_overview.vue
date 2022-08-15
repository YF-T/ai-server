<template>
    <div class="context">
        <div class="args">
          <div class="inputblock">
            <label>输入变量</label>
            <span style="white-space:pre">   </span><span class="line"></span>
            <table>
              <tr>
                <th width="30%">字段</th>
                <th width="15%">类型</th>
                <th width="20%">测量</th>
                <th width="35%">取值</th>
              </tr>
              <!-- {% for %} -->
              <tr>
                <td>字段</td>
                <td>类型</td>
                <td>测量</td>
                <td>取值</td>
              </tr>
              <!-- {% endfor %} -->
            </table>
          </div>
          <div class="outputblock">
            <label>输出变量</label>
            <span style="white-space:pre">   </span><span class="line"></span>
            <table>
              <tr>
                <th>字段</th>
                <th>类型</th>
                <th>测量</th>
                <th>取值</th>
              </tr>
              <!-- {% for %} -->
              <tr>
                <td>字段</td>
                <td>类型</td>
                <td>测量</td>
                <td>取值</td>
              </tr>
              <!-- {% endfor %} -->
            </table>
          </div>
        </div>
        
        <div class="evalute">
          <label>评估结果</label>
          <span style="white-space:pre">   </span><span class="line"></span>

          <div>

          </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'model_info_overview',
  props: {
    msg: String,
  },
});
</script>

<style scoped>
.context {
    height: 500px;
    width: auto;
    background: #F1F2F6;
}

.args{
  display: flex;
}

label {
  position: relative;
  left:10px;
  font-weight: bold;
  font-size: 30px;
}

.inputblock, .outputblock{
  flex-grow:1;
  display:block;
  margin: 20px;
  height: 200px;
  overflow: auto;
  background: white;
  text-align:left;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
}

table{
  width: 100%;
  background: white;
}

table th{
  background: #FAFAFA;
}
.evalute{
  display: block;
  margin: 20px;
  height: 200px;
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

</style>
