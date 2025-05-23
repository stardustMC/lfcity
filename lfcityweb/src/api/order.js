import {computed, reactive} from "vue";
import http from "../utils/http.js";


const order = reactive({
    course_list: [],     // 购物车中勾选的课程列表
    user_coupon: false,     // 用户是否使用优惠
    discount_type: -1,    // -1表示未使用优惠，0表示优惠券，1表示积分
    coupon_list: [],     // 用户拥有的可用优惠券列表
    coupon: -1,          // 当前用户选中的优惠券下标
    credit: 0,           // 当前用户选择抵扣的积分
    total_credit: 0,    // 用户拥有的积分
    credit_ratio: 0,    // 积分换算价格比例
    fixed: true,         // 底部订单总价是否固定浮动
    pay_type: 0,         // 支付方式
    discount_price: 0,   // （优惠券或积分）优惠金额

    timeout: 60 * 15,   // 订单支付倒计时
    timer: null,        // 倒计时计时器
    loading: false,      // 等待支付中
    order_number: "",   // 订单号

    total_price: computed(()=>{
        let total = 0.0;
        order.course_list.forEach(course=>{
            total += course.discount.price || course.price;
        })
        return total;
    }),
    max_use_credits: computed(()=>{
        let max_credit = 0;
        order.course_list.forEach(course=>{
            if(!course.discount.price) max_credit += course.credits;
        });
        return Math.min(max_credit, order.total_credit);
    }),
    credit_course_list: computed(()=>{
       return order.course_list.filter(course=>!course.discount.price);
    }),
    get_selected_cart_list(token){
        return http.get("/cart/list/", {
            headers: {
                Authorization: "jwt " + token
            },
            params: {
                selected: true
            }
        })
    },
    commit_order(token) {
        let data = {
            pay_type: this.pay_type,
            discount_type: this.discount_type,
            user_coupon_id: -1,
            credit: this.credit,
        };
        if(this.discount_type === 0 && this.coupon > -1) data.user_coupon_id = this.coupon_list[this.coupon].user_coupon_id;
        return http.post("/order/", data, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    get_enable_coupons(token){
        return http.get("/coupon/enable/", {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    alipay_page(token){
        return http.get(`/payment/alipay/link/${this.order_number}/`, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    query_order(token){
        return http.get(`/payment/alipay/query/${this.order_number}/`, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
})

const detail = reactive({
    pay_time: "",
    real_price: 0.0,
    courses: [],
    alipay_feedback(token){
        let query_string = window.location.search;
        return http.get(`/payment/alipay/result/${query_string}`, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
})

export {order, detail};