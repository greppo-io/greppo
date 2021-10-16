import Vue from "vue";
import App from "./App.vue";
import store from "./store";

// For unicons
import "./components/utils/include-unicons.js";

// For full screen : https://github.com/mirari/vue-fullscreen
import VueFullscreen from "vue-fullscreen";
Vue.use(VueFullscreen);

Vue.config.productionTip = false;

new Vue({
    store,
    render: (h) => h(App),
}).$mount("#app");
