import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'element-plus/dist/index.css';

import router from "./router/index.js";
import store from "./store/index.js"


createApp(App).use(store).use(router).mount('#app')
