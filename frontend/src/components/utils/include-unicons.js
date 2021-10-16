import Vue from "vue";
import Unicon from "vue-unicons/dist/vue-unicons-vue2.umd";
import {
    uniEstate,
    uniExpandArrowsAlt,
    uniCompressArrows,
    uniAngleRight,
    uniAngleLeft,
    uniAngleDown,
} from "vue-unicons/dist/icons";

Unicon.add([
    uniEstate,
    uniExpandArrowsAlt,
    uniCompressArrows,
    uniAngleRight,
    uniAngleLeft,
    uniAngleDown,
]);
Vue.use(Unicon);
