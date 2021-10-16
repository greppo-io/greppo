<template>
    <div>
        <fullscreen
            :fullscreen.sync="isFullScreen"
            :teleport="teleport"
            :page-only="pageOnly"
        >
            <loading-screen v-if="getStatus === 1" />
            <div class="flex bg-gray-50">
                <!-- Left Side Bar  -->
                <div class="flex relative">
                    <div
                        class="flex flex-col h-screen sidebar sidebar-width"
                        v-show="leftContainerOpen"
                    >
                        <!-- Left Side Bar Content  -->
                        <left-container />
                    </div>
                    <div
                        @click="toggleLeftContainer"
                        class="sidebar-control h-8 w-4 bg-gray-700 mt-2 -mr-4 absolute top-0 right-0 flex items-center rounded-tr rounded-br justify-center cursor-pointer"
                    >
                        <unicon
                            name="angle-left"
                            fill="white"
                            v-show="leftContainerOpen"
                        ></unicon>
                        <unicon
                            name="angle-right"
                            fill="white"
                            v-show="!leftContainerOpen"
                        ></unicon>
                    </div>
                </div>

                <!-- Center Container  -->
                <div class="flex flex-col w-full h-screen">
                    <div class="h-full">
                        <!-- Center Container Content  -->
                        <center-container
                            v-if="getComponentStatus.mapComponent"
                            ref="centercontainer"
                            :isFullScreen="isFullScreen"
                            @toggle-fullscreen="toggleFullScreen"
                        />
                    </div>
                </div>

                <!-- Right Side Bar  -->
                <div class="flex relative" v-if="false">
                    <!-- Right Side Bar Control -->
                    <div
                        @click="toggleRightContainer"
                        class="sidebar-control h-10 w-10 bg-white absolute mt-2 -ml-10 flex items-center rounded-tl rounded-bl justify-center cursor-pointer"
                    >
                        <unicon name="analytics" fill="black"></unicon>
                    </div>

                    <div
                        class="flex flex-col w-96 h-screen sidebar"
                        v-show="rightContainerOpen"
                    >
                        <right-container />
                    </div>
                </div>
            </div>
        </fullscreen>
    </div>
</template>

<script>
import CenterContainer from "./CenterContainer";
import LeftContainer from "./LeftContainer";
import RightContainer from "./RightContainer";
import { mapGetters } from "vuex";
import LoadingScreen from "./functional-components/LoadingScreen.vue";

export default {
    name: "BaseContainer",
    components: {
        CenterContainer,
        LeftContainer,
        RightContainer,
        LoadingScreen,
    },
    data() {
        return {
            leftContainerOpen: true,
            rightContainerOpen: false,
            isFullScreen: false,
            teleport: true,
            pageOnly: false,
        };
    },
    methods: {
        toggleFullScreen() {
            this.isFullScreen = !this.isFullScreen;
            if (this.getComponentStatus.mapComponent) {
                this.$refs.centercontainer.resetMapContainerSize();
            }
        },
        toggleLeftContainer() {
            this.leftContainerOpen = !this.leftContainerOpen;
            if (this.getComponentStatus.mapComponent) {
                this.$refs.centercontainer.resetMapContainerSize();
            }
        },
        toggleRightContainer() {
            this.rightContainerOpen = !this.rightContainerOpen;
            if (this.getComponentStatus.mapComponent) {
                this.$refs.centercontainer.resetMapContainerSize();
            }
        },
    },
    computed: {
        ...mapGetters(["getStatus", "getComponentStatus"]),
        // statusWatcher() {
        //     try {
        //         return this.getStatus;
        //     } catch (error) {
        //         return 0;
        //     }
        // },
    },
    watch: {
        // TODO get the setView to apply the the zoom and center when the data and map is loaded.
        // statusWatcher(newVal) {
        //     if (this.getComponentStatus.mapComponent) {
        //         if (newVal === 2) {
        //             this.$refs.centercontainer.resetViewHandler();
        //         }
        //     }
        // },
    },
};
</script>

<style scoped>
.sidebar,
.sidebar-control {
    z-index: 1100;
}
.sidebar-width {    
    width: 33vw;
    min-width: 340px;
}

</style>
