<template>
  <div class="title">
    <span :class="{active:state.login_type===0}" @click="state.login_type=0">密码登录</span>
    <span :class="{active:state.login_type===1}" @click="state.login_type=1">短信登录</span>
  </div>
  <div class="inp" v-if="state.login_type===0">
    <input v-model="user.username" type="text" placeholder="用户名 / 手机号码" class="user">
    <input v-model="user.password" type="password" class="pwd" placeholder="密码">
    <div id="geetest1"></div>
    <div class="rember">
      <label>
        <input type="checkbox" class="no" name="a" v-model="state.save_state"/>
        <span>记住账户</span>
      </label>
      <p>忘记密码</p>
    </div>
    <button class="login_btn" @click="login">登录</button>
    <p class="go_login">没有账号<router-link to="/register"><span>立即注册</span></router-link></p>
  </div>
  <div class="inp" v-show="state.login_type===1">
    <input v-model="state.username" type="text" placeholder="手机号码" class="user">
    <input v-model="state.password"  type="text" class="code" placeholder="短信验证码">
    <el-button id="get_code" type="primary">获取验证码</el-button>
    <button class="login_btn">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
</template>

<script setup>
import {reactive} from "vue";
import store from "../store/index.js"
import user from "../api/user.js"
import {ElMessage} from "element-plus";

// 发送一个登录成功的信号给父组件
const emit = defineEmits(['login_success'])

const state = reactive({
  login_type: 0,
  save_state: false,
})

const login = () => {
  user.login().then(response => {
    let token = response.data.token;
    if (state.save_state) {
      sessionStorage.removeItem("token");
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
      sessionStorage.setItem("token", token);
    }

    let payload = token.split(".")[1];
    let payload_json = JSON.parse(atob(payload));
    store.commit("login", payload_json);
    store.commit("cart_count", response.data.cart_count)

    // 清空api的user对象
    user.username = "";
    user.password = "";
    user.phone = "";
    user.code = "";
    emit("login_success");

    ElMessage.success("登录成功^_^");
  }).catch(error => {
    console.log(error)
    ElMessage.error("登录失败啦...")
  })
}

</script>

<style scoped>
.title{
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 0px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}
.title span.active{
	color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp .code{
    width: 220px;
    margin-right: 16px;
}
#get_code{
   margin-top: 6px;
}
.inp input{
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
    vertical-align: middle;
    margin-right: 4px;
}

.inp .rember p span{
    display: inline-block;
    font-size: 12px;
    width: 100px;
}
.login_btn{
    cursor: pointer;
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
    border: none;
    outline: none;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>