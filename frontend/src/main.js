import Vue from "vue";
import App from "./App.vue";
import store from "./store";

// For unicons
import "./components/utils/include-unicons.js";

// toggle-button : https://github.com/euvl/vue-js-toggle-button
import { ToggleButton } from "vue-js-toggle-button";
Vue.component("ToggleButton", ToggleButton);

// markdown to html : https://github.com/meteorlxy/vue-showdown
import VueShowdown from "vue-showdown";
Vue.use(VueShowdown);

Vue.config.productionTip = false;

new Vue({
    store,
    render: (h) => h(App),
}).$mount("#app");
