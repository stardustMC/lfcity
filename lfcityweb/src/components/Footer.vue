<template>
    <div class="footer">
      <ul>
        <li v-for="item in nav.footer_list">
          <router-link :to="item.link">{{ item.name }}</router-link>
        </li>
      </ul>
      <p>Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p>
    </div>
</template>

<script setup>
import nav from "../api/nav.js";

const get_footer_list = ()=>{
  nav.get_footer_list();
}
get_footer_list();
</script>

<style scoped>
.footer {
  width: 100%;
  height: 128px;
  color: #545C63;
}
.footer ul{
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 930px;
}
.footer ul li{
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}
.footer ul::after{
  content:"";
  display:block;
  clear:both;
}
.footer p{
  text-align: center;
  font-size: 12px;
}
</style>