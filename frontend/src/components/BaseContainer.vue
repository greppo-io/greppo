<template>
    <div>
        <app-info-modal v-if="getAppInfo.modal" />
        <error-modal v-if="getErrorInfo.modal"/>
        <div class="flex bg-gray-50">
            <!-- Left Side Bar  -->
            <left-container />

            <!-- Center Container  -->
            <center-container />

            <!-- Right Side Bar  -->
            <right-container />
        </div>
    </div>
</template>

<script>
import CenterContainer from "./CenterContainer.vue";
import LeftContainer from "./LeftContainer";
import RightContainer from "./RightContainer";
import { mapGetters } from "vuex";
import AppInfoModal from "./functional-components/AppInfoModal.vue";
import ErrorModal from './functional-components/ErrorModal.vue';

export default {
    name: "BaseContainer",
    components: {
        CenterContainer,
        LeftContainer,
        RightContainer,
        AppInfoModal,
        ErrorModal,
    },
    computed: {
        ...mapGetters(["getComponentStatus", "getAppInfo", "getErrorInfo"]),
    },
};
</script>

<style></style>
