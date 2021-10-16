import Vuex from "vuex";
import Vue from "vue";

import BackendAPI from "./modules/backend-api";

// Load Vuex
Vue.use(Vuex);

// Create store
export default new Vuex.Store({
    modules: {
        BackendAPI,
    },
});
