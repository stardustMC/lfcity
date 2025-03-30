<template>
  <div class="home">
    <Header></Header>
    <h1>首页</h1>
    <el-button type="primary">主要按钮</el-button>
    <el-button type="success">成功按钮</el-button>
    <Footer></Footer>
  </div>
</template>

<script setup>
import http from '../utils/http.js'

// http.get("/home/").then(response=>{
//   console.log(response.data);
// })
</script>


<style scoped>

</style>