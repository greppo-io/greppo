<template>
    <div>
        <fullscreen
            :fullscreen.sync="isFullScreen"
            :teleport="teleport"
            :page-only="pageOnly"
        >
            <app-info-modal v-if="getAppInfo.modal" />
            <div class="flex bg-gray-50">
                <!-- Left Side Bar  -->
                <left-container />

                <!-- Center Container  -->
                <center-container />

                <!-- Right Side Bar  -->
                <right-container />
            </div>
        </fullscreen>
    </div>
</template>

<script>
import CenterContainer from "./CenterContainer.vue";
import LeftContainer from "./LeftContainer";
import RightContainer from "./RightContainer";
import { mapGetters } from "vuex";
import { eventHub } from "src/event-hub";
import AppInfoModal from "./functional-components/AppInfoModal.vue";

export default {
    name: "BaseContainer",
    components: {
        CenterContainer,
        LeftContainer,
        RightContainer,
        AppInfoModal,
    },
    data() {
        return {
            isFullScreen: false,
            teleport: true,
            pageOnly: false,
        };
    },
    methods: {
        toggleFullScreen() {
            this.isFullScreen = !this.isFullScreen;
            if (this.getComponentStatus.mapComponent) {
                eventHub.$emit("resetMapContainerSize");
            }
        },
    },
    computed: {
        ...mapGetters(["getComponentStatus", "getAppInfo"]),
    },
};
</script>

<style></style>
