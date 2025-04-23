import {computed, reactive} from "vue";
import http from "../utils/http.js"

const course = reactive({
    page: 1,
    size: 5,
    count:0,
    ordering: "id",
    ordering_list: ['id', 'order', 'students'],
    direction: -1,
    direction_list: [],
    category: -1,
    category_list: [],
    course_list: [],
    timer: null,
    text: "",
    get_directions(){
        return http.get("/course/directions/");
    },
    get_categories(){
        return http.get(`/course/categories/${this.direction}/`);
    },
    get_course_list(){
        let params = {
            page: this.page,
            size: this.size,
            ordering: this.ordering,
        };
        return http.get(`/course/${this.direction}/${this.category}/`, {
            params
        });
    },
    search_course(){
        let params = {
            text: this.text,
            page: this.page,
            size: this.size,
            ordering: this.ordering,
        }
        return http.get(`/course/search/`, {
            params
        })
    },
    start_timer(){
        clearInterval(this.timer);
        setInterval(()=>{
            this.course_list.forEach((course)=>{
                if(course.discount.expire && course.discount.expire > 0){
                    course.discount.expire--;
                }
            });
        }, 1000);
    }
});

const detail = reactive({
    id: 1,
    timer: null,
    info: {},
    get_course_detail(){
        return http.get(`/course/detail/${this.id}/`);
    },
    start_timer(){
        clearInterval(this.timer);
        setInterval(()=>{
            if(detail.info.discount.expire){
                if(detail.info.discount.expire > 0) detail.info.discount.expire--;
                else{
                    clearInterval(detail.timer);
                    detail.info.discount = null;
                }
            }
        }, 1000);
    },
    total_duration: computed(()=>{
        let total = 0;
        // if(detail.info.chapter_list)
        detail.info.chapter_list?.forEach(chapter=>{
            chapter.lesson_list?.forEach(lesson=>{
                let duration = lesson.duration.split(":");
                let minute = parseInt(duration[0]), second = parseInt(duration[1]);
                total += minute * 60 + second;
            })
        })
        return total;
    }),
})

export {course, detail};