<template>
  <div class="course">
    <Header></Header>
    <div class="top-wrap">
        <div class="actual-header">
            <div class="actual-header-wrap">
                <div class="banner">
                    <router-link class="title" to="/course"><img class="h100" src="../assets/coding-title.png" alt=""></router-link>
                    <div>真实项目实战演练</div>
                </div>
                <div class="actual-header-search">
                    <div class="search-inner">
                        <input class="actual-search-input" v-model="course.text" placeholder="搜索感兴趣的实战课程内容" type="text" autocomplete="off">
                        <span @click="search_course">
                          <img class="actual-search-button" src="../assets/search.svg" alt="搜索" />
                        </span>
                    </div>
                    <div class="actual-searchtags">
                    </div>
                    <div class="search-hot">
                        <span>热搜：</span>
                        <a href="">Java工程师</a>
                        <a href="">Vue</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="type">
            <div class="type-wrap">
                <div class="one warp">
                    <span class="name">方向：</span>
                    <ul class="items">
                        <li :class="{cur:course.direction===-1}" @click.prevent.stop="course.direction=-1"><a href="">全部</a></li>
                        <li :class="{cur:course.direction===direction.id}" @click.prevent.stop="course.direction=direction.id" v-for="direction in course.direction_list">
                          <a href="">{{direction.name}}</a>
                        </li>
                    </ul>
                </div>
                <div class="two warp">
                    <span class="name">分类：</span>
                    <ul class="items">
                        <li :class="{cur:course.category===-1}" @click.prevent.stop="course.category=-1"><a href="">不限</a></li>
                        <li :class="{cur:course.category===category.id}" @click.prevent.stop="course.category=category.id" v-for="category in course.category_list">
                          <a href="">{{category.name}}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="main">
        <div class="main-wrap">
            <div class="filter clearfix">
                <div class="sort l">
                  <!-- TODO: 通过后端接口获取排序字段，并实现升序和倒序（点击切换） -->
                  <a href="" :class="{on:course.ordering==='id'}" @click.prevent.stop="course.ordering='id'">默认</a>
                  <a href="" :class="{on:course.ordering==='order'}" @click.prevent.stop="course.ordering='order'">最新</a>
                  <a href="" :class="{on:course.ordering==='students'}" @click.prevent.stop="course.ordering='students'">销量</a>
                </div>
                <div class="other r clearfix"><a class="course-line l" href="" target="_blank">学习路线</a></div>
            </div>
            <ul class="course-list clearfix">
              <li class="course-card" v-for="info in course.course_list">
                <router-link :to="{name: 'Detail', params: {id: info.id}}">
                    <div class="img"><img :src="info.course_cover" alt=""></div>
                    <p class="title ellipsis2">{{info.name}}</p>
                    <p class="one">
                        <span>{{info.students}}人报名</span>
                        <span class="discount r" v-if="info.discount.price">
                          <i class="name" v-if="info.discount.name">{{info.discount.name}}</i>
                          <i class="countdown" v-if="info.discount.expire">{{format_date(info.discount.expire)}}</i>
<!--                          <i class="name">优惠价</i>-->
                        </span>
                    </p>
                    <p class="two clearfix">
                        <span class="price l red bold" v-if="info.discount.price">￥{{info.discount.price}}</span>
                        <span class="price l red bold" v-else>￥{{info.price}}</span>
                        <span class="origin-price l delete-line" v-if="info.discount.price">￥{{info.price}}</span>
                        <span class="add-shop-cart r" @click.prevent="add_course_to_cart(info.id)"><img class="icon imv2-shopping-cart" src="../assets/cart2.svg">加购物车</span>
                    </p>
                </router-link>
              </li>

            </ul>
          <el-pagination
              background
              layout="total, sizes, prev, pager, next, jumper"
              :size="'large'"
              v-model:current-page="course.page"
              v-model:page-size="course.size"
              :total="course.count"
              :page-sizes="[3, 5, 10]"
              @current-change="page_change"
              @size-change="size_change"
          >
          </el-pagination>
        </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script setup>
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {course} from "../api/course.js"
import cart from "../api/cart.js"
import {watch} from "vue";

import {format_date} from "../utils/helper.js";
import {ElMessage} from "element-plus";
import store from "../store/index.js";

const get_course_directions = ()=>{
  course.get_directions().then(response=>{
    course.direction_list = response.data;
  })
};
get_course_directions();

const get_course_categories = ()=>{
  course.get_categories().then(response=>{
    course.category_list = response.data;
  })
};
get_course_categories();

const get_course_list = ()=>{
  course.get_course_list().then(response=>{
    // console.log(response.data.results);
    course.course_list = response.data.results;
    course.count = response.data.count;
    course.start_timer();
  })
};
get_course_list();

const search_course = ()=>{
  if(!course.text){
    ElMessage.warning("搜索内容不能为空");
    return
  }
  course.search_course().then(response=>{
    // console.log(response.data.results);
    course.course_list = response.data.results;
    course.count = response.data.count;
    course.start_timer();
  }).catch(error=>{
    ElMessage.error(error.response.data.message);
  })
};

const page_change = (page)=>{
  course.page = page;
}

const size_change = (size)=>{
  course.size = size;
  if(course.page === 1) get_course_list();
  else course.page = 1;
}

watch(()=>course.page, ()=>{
  get_course_list();
})

watch(()=>course.direction, ()=>{
  get_course_categories();
  if(course.category === -1) get_course_list();
  else course.category = -1;
})

watch(()=>course.category, ()=>{
  get_course_list();
})

watch(()=>course.ordering, ()=>{
  get_course_list();
})

const add_course_to_cart = (course_id)=>{
  let token = localStorage.getItem("token") || sessionStorage.getItem("token");
  cart.add_course(token, course_id).then(response=>{
    store.commit("cart_count", response.data.cart_count);
    ElMessage.success(response.data.message);
  }).catch(error=>{
    console.log(error);
    ElMessage.info(error.response.data.message);
  })
}

</script>

<style scoped>
.top-wrap {
	background-color: #f5f7fa;
	background-repeat: no-repeat;
	background-position: top center;
	background-size: cover
}
.actual-header{
  max-width: 1500px;
  margin: 0 auto;
}
.actual-header .actual-header-wrap {
	height: 100%;
	display: -webkit-box;
	display: -ms-flexbox;
	display: -webkit-flex;
	display: flex;
	-webkit-box-align: center;
	-ms-flex-align: center;
	-webkit-align-items: center;
	align-items: center;
	-webkit-box-pack: justify;
	-ms-flex-pack: justify;
	-webkit-justify-content: space-between;
	justify-content: space-between;
	padding-top: 8px
}

.actual-header .actual-header-wrap .banner {
	display: -webkit-box;
	display: -ms-flexbox;
	display: -webkit-flex;
	display: flex;
	-webkit-box-align: center;
	-ms-flex-align: center;
	-webkit-align-items: center;
	align-items: center
}

.actual-header .actual-header-wrap .banner .title {
	height: 46px;
	margin-right: 8px
}

.actual-header .actual-header-wrap .actual-header-search {
	position: relative;
	width: 320px
}

.actual-header .actual-header-wrap .actual-header-search .search-inner {
	width: 100%;
	border-radius: 4px;
	overflow: hidden;
	margin: 17px 0 7px;
	border: 1px solid rgba(84,92,99,.2)
}

.actual-header .actual-header-wrap .actual-header-search .search-inner .actual-search-input {
	width: 275px;
	font-size: 12px;
	color: #93999f;
	line-height: 24px;
	padding: 5px 12px;
	border: none;
	border-radius: 0;
	box-sizing: border-box;
	background: 0 0
}

.actual-header .actual-header-wrap .actual-header-search .search-inner .actual-search-input::-webkit-input-placeholder {
	color: #9199a1
}

.actual-header .actual-header-wrap .actual-header-search .search-inner .actual-search-input::-moz-placeholder {
	color: #9199a1
}

.actual-header .actual-header-wrap .actual-header-search .search-inner .actual-search-input:-moz-placeholder {
	color: #9199a1
}

.actual-header .actual-header-wrap .actual-header-search .search-inner .actual-search-input:-ms-input-placeholder {
	color: #9199a1
}

.actual-header .actual-header-wrap .actual-header-search .search-inner .actual-search-button {
  width: 26px;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-right: 4px;
  padding-left: 6px;
  height: 26px;
  font-size: 18px;
  text-align: center;
  line-height: 26px;
	color: #fff;
  background-color: rgba(84,92,99,.2);
	cursor: pointer;
	border-top-right-radius: 4px;
	border-bottom-right-radius: 4px;
	float: right
}

.actual-header .actual-header-wrap .actual-header-search .actual-searchtags {
	position: absolute;
	right: 128px;
	top: 0;
	height: 48px;
	line-height: 48px;
	text-align: right
}

.actual-header .actual-header-wrap .actual-header-search .actual-searchtags a {
	margin-left: 24px;
	font-size: 12px;
	color: #4d555d;
	line-height: 48px
}

.actual-header .actual-header-wrap .actual-header-search .actual-searchtags a:hover {
	color: #f01414
}

.actual-header .actual-header-wrap .actual-header-search .actual-history-item a {
	float: left;
	font-size: 12px;
	color: rgba(7,17,27,.6);
	line-height: 16px;
	padding: 4px 12px;
	margin-right: 8px;
	background: rgba(7,17,27,.05);
	border-radius: 12px;
	transition: .3s background,color linear;
	margin-top: 8px
}

.actual-header .actual-header-wrap .actual-header-search .actual-history-item a:hover {
	background: rgba(7,17,27,.1);
	color: #07111b
}

.actual-header .actual-header-wrap .actual-header-search li {
	display: block;
	width: 100%;
	height: 48px;
	transition: .3s background linear;
	padding: 12px 16px;
	box-sizing: border-box;
	font-size: 14px;
	color: #4d555d;
	line-height: 24px;
	cursor: pointer;
	z-index: 1
}

.actual-header .actual-header-wrap .actual-header-search li:hover {
	background: #f3f5f7;
	color: #07111b
}

.actual-header .actual-header-wrap .actual-header-search .search-hot {
	height: 21px;
	overflow: hidden;
	padding-left: 14px
}

.actual-header .actual-header-wrap .actual-header-search .search-hot a,
.actual-header .actual-header-wrap .actual-header-search .search-hot span {
	color: rgba(84,92,99,.7);
	font-size: 12px;
	line-height: 16px
}

.actual-header .actual-header-wrap .actual-header-search .search-hot a {
	margin-right: 14px
}

.actual-header .actual-header-wrap .actual-header-search .search-hot a:last-child {
	margin-right: 0
}

.type {
  max-width: 1500px;
  margin: 0 auto;
	padding-bottom: 27px
}

.type .type-wrap {
	position: relative;
	height: 109px
}

.type .type-wrap .warp {
	display: -webkit-box;
	display: -ms-flexbox;
	display: -webkit-flex;
	display: flex;
	position: absolute;
	width: 1430px;
	height: 54px;
	overflow: hidden;
	padding: 10px;
	box-sizing: border-box;
	box-shadow: 0 12px 20px 0 rgba(95,101,105,0);
	border-radius: 8px;
	transition: all .2s
}

.type .type-wrap .warp.one {
	margin-bottom: 25px;
	z-index: 3
}

.type .type-wrap .warp.two {
	top: 59px;
	z-index: 2
}

.type .type-wrap .warp .name {
	width: 3em;
	color: #07111b;
	line-height: 32px;
	font-weight: 700;
	margin-right: 6px
}

.type .type-wrap .warp .items {
	width: 0;
	-webkit-box-flex: 1;
	-ms-flex: 1;
	-webkit-flex: 1;
	flex: 1
}

.type .type-wrap .warp .items li {
	float: left;
	line-height: 16px;
	padding: 8px;
	border-radius: 6px;
	margin: 0 12px 12px 0
}

.type .type-wrap .warp .items li a {
	color: #1c1f21
}

.type .type-wrap .warp .items li.cur {
	background-color: rgba(233,142,70,.1)
}

.type .type-wrap .warp .items li.cur a {
	color: #e98e46
}
.delete-line{
  text-decoration: line-through;
}
/******** 课程列表 ********/
.l{
  float: left;
}
.r{
  float: right;
}
.red{
  color: red;
}
.bold{
  font-weight: 700;
}
.main {
	margin-bottom: 60px
}
.main .main-wrap{
  max-width: 1500px;
  margin: 0 auto;
}
.clearfix:after {
	content: '';
	display: block;
	height: 0;
	clear: both;
	visibility: hidden
}

.main .filter {
	margin: 20px 0
}

.main .filter .sort {
	overflow: hidden
}

.main .filter .sort a {
	display: inline-block;
	float: left;
	font-size: 12px;
	color: #545c63;
	line-height: 16px;
	padding: 4px 12px;
	border-radius: 100px;
	margin-right: 12px
}

.main .filter .sort a:last-child {
	margin-right: 0
}

.main .filter .sort a.on {
	color: #fff;
	background-color: #545c63
}

.main .filter .other {
	font-size: 12px
}

.main .filter .other .course-line {
	color: #e98e46;
	line-height: 16px;
	padding: 4px 16px;
	border-radius: 100px;
	background-color: rgba(233,142,70,.1);
	margin-left: 24px
}

.main .course-list .course-card {
	position: relative;
	width: 270px;
	height: 270px;
	float: left;
	margin: 0 37px 20px 0;
	box-shadow: 0 4px 8px 0 rgba(95,101,105,.05);
	border-radius: 8px;
	background-color: #fff;
	transition: transform .2s,box-shadow .2s
}

.main .course-list .course-card:nth-child(5n) {
	margin-right: 0
}

.main .course-list .course-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 12px 20px 0 rgba(95,101,105,.1)
}

.main .course-list .course-card a {
	display: inline-block;
	width: 100%
}

.main .course-list .course-card .img {
	height: 152px;
	background: no-repeat center/cover;
	margin-bottom: 8px;
	border-radius: 8px 8px 0 0;
	overflow: hidden
}

.main .course-list .course-card .title {
	color: #545c63;
	line-height: 20px;
	height: 40px;
	margin-bottom: 8px;
	padding: 0 8px
}

.main .course-list .course-card .title.ellipsis2 {
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical
}

.main .course-list .course-card .one,
.main .course-list .course-card .two {
	font-size: 12px;
	color: #9199a1;
	line-height: 18px;
	padding: 0 8px;
	margin-bottom: 8px
}

.main .course-list .course-card .one .add-shop-cart .icon,
.main .course-list .course-card .one .star .icon,
.main .course-list .course-card .two .add-shop-cart .icon,
.main .course-list .course-card .two .star .icon {
	display: inline-block;
	margin-right: 2px;
	font-size: 14px
}
.imv2-shopping-cart{
  width: 14px;
}
.main .course-list .course-card .one .add-shop-cart.add-shop-cart,
.main .course-list .course-card .one .add-shop-cart.stared,
.main .course-list .course-card .one .star.add-shop-cart,
.main .course-list .course-card .one .star.stared,
.main .course-list .course-card .two .add-shop-cart.add-shop-cart,
.main .course-list .course-card .two .add-shop-cart.stared,
.main .course-list .course-card .two .star.add-shop-cart,
.main .course-list .course-card .two .star.stared {
	color: #ff655d
}


.main .course-list .course-card .one .discount i,
.main .course-list .course-card .two .discount i {
	font-style: normal;
	padding: 3px 4px
}

.main .course-list .course-card .one .discount i.name,
.main .course-list .course-card .two .discount i.name {
	color: #fff;
	background-color: rgba(242,13,13,.6)
}

.main .course-list .course-card .one .price,
.main .course-list .course-card .two .price {
	line-height: 20px;
	margin-right: 2px
}

.main .course-list .course-card .one .discount,
.main .course-list .course-card .two .discount {
	border: 1px solid rgba(242,13,13,.2);
	border-radius: 2px;
	font-size: 12px;
	line-height: 1;
	margin-right: 4px;
	overflow: hidden;
	display: -webkit-box;
	display: -ms-flexbox;
	display: -webkit-flex;
	display: flex;
	-webkit-box-align: center;
	-ms-flex-align: center;
	-webkit-align-items: center;
	align-items: center
}

.main .course-list .course-card .one .discount i,
.main .course-list .course-card .two .discount i {
	font-style: normal;
	padding: 3px 4px
}

.main .course-list .course-card .one .discount i.name,
.main .course-list .course-card .two .discount i.name {
	color: #fff;
	background-color: rgba(242,13,13,.6)
}

.main .course-list .course-card .one .discount i.countdown,
.main .course-list .course-card .two .discount i.countdown {
	display: flex;
	font-family: DINCondensed,'微软雅黑';
	color: #f76e6e;
	padding-top: 4px;
	padding-bottom: 2px
}

.main .course-list .course-card .one .discount i.countdown .day,
.main .course-list .course-card .two .discount i.countdown .day {
	display: inline-block;
	width: 12px;
	height: 12px;
  transform:scale(0.8);
}


/**** 页码 *****/
.page {
	margin: 25px 0 auto;
	overflow: hidden;
	clear: both;
	text-align: center
}

.page a {
	display: inline-block;
	margin: 0 12px;
	width: 36px;
	height: 36px;
	line-height: 36px;
	font-size: 14px;
	color: #4d555d;
	text-align: center;
	border-radius: 50%;
	-webkit-transition: border-color .2s;
	-moz-transition: border-color .2s;
	transition: border-color .2s
}

.page a:hover {
	text-decoration: none;
	background-color: #d9dde1
}

.page a.active {
	background: #4d555d;
	color: #fff
}

.page a:first-child,
.page a:last-child,
.page a:nth-child(2),
.page a:nth-last-child(2) {
	width: auto
}

.page a:first-child:hover,
.page a:last-child:hover,
.page a:nth-child(2):hover,
.page a:nth-last-child(2):hover {
	background-color: transparent
}

.page span {
	display: inline-block;
	padding: 0 12px;
	min-width: 20px;
	height: 39px;
	line-height: 39px;
	font-size: 14px;
	color: #93999f;
	text-align: center
}
</style>