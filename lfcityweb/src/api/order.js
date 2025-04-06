import {computed, reactive} from "vue";
import http from "../utils/http.js";


const order = reactive({
    course_list: [],     // 购物车中勾选的课程列表
    discount_type: -1,    // -1表示未使用优惠，0表示优惠券，1表示积分
    coupon_list: [],     // 用户拥有的可用优惠券列表
    coupon: -1,          // 当前用户选中的优惠券下标
    credit: 0,           // 当前用户选择抵扣的积分
    fixed: true,         // 底部订单总价是否固定浮动
    pay_type: 0,         // 支付方式
    discount_price: 0,   // （优惠券或积分）优惠金额
    total_price: computed(()=>{
        let total = 0.0;
        order.course_list.forEach(course=>{
            total += course.discount.price || course.price;
        })
        return total;
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
})

export {order};