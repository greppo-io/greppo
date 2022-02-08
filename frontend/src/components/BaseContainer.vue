<template>
    <div>
        <app-info-modal v-if="getAppInfo.modal" />
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

export default {
    name: "BaseContainer",
    components: {
        CenterContainer,
        LeftContainer,
        RightContainer,
        AppInfoModal,
    },
    computed: {
        ...mapGetters(["getComponentStatus", "getAppInfo"]),
    },
};
</script>

<style></style>
