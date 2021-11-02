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
                    <!-- Left Side Bar Control  -->
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
                    <div class="h-full relative">
                        <!-- Center Container Content  -->
                        <map-container
                            v-if="getComponentStatus.mapComponent"
                            ref="centercontainer"
                            :isFullScreen="isFullScreen"
                            @toggle-fullscreen="toggleFullScreen"
                        />

                        <div
                            class="absolute top-0 right-3 bg-white bg-opacity-70 rounded-b-md px-2 py-1"
                            style="z-index: 1500;"
                        >
                            <div class="flex flex-row items-center">
                                <div class="text-center text-gray-700">
                                    <p style="font-size: 0.70em;">made with</p>
                                    <a
                                        class="flex flex-row mt-1 items-center"
                                        href="https://greppo.io"
                                        target="_blank"
                                        ><img
                                            src="../assets/logo.svg"
                                            class="mx-1"
                                            width="20px"
                                        />
                                        <p class="text-base mx-1">Greppo</p>
                                    </a>
                                </div>
                                <div class="ml-2">
                                    <button
                                        class="flex items-end relative hover:bg-gray-200 rounded "
                                        @click="dropdownInfo = !dropdownInfo"
                                    >
                                        <unicon
                                            name="info-circle"
                                            fill="gray"
                                            class="m-1"
                                            width="20px"
                                        ></unicon>
                                    </button>
                                    <div
                                        v-show="dropdownInfo"
                                        @click="dropdownInfo = false"
                                        class="fixed inset-0 h-screen w-screen z-10"
                                    ></div>
                                    <div
                                        v-show="dropdownInfo"
                                        class="absolute top-14 right-0 w-48 bg-white bg-opacity-70 rounded-md overflow-hidden shadow-lg z-20"
                                    >
                                        <a
                                            href="#"
                                            class="block px-4 py-3 font-medium text-gray-800 border-b"
                                            >Made with Greppo
                                        </a>
                                        <a
                                            href="https://docs.greppo.io/"
                                            target="_blank"
                                            class="block px-4 py-3 text-sm text-gray-800 hover:bg-gray-200"
                                            >Documentation</a
                                        >
                                        <a
                                            href="https://greppo.io/"
                                            target="_blank"
                                            class="block px-4 py-3 text-sm text-gray-800 hover:bg-gray-200"
                                            >Website - greppo.io</a
                                        >
                                        <a
                                            href="https://github.com/greppo-io/greppo"
                                            target="_blank"
                                            class="block px-4 py-3 text-sm text-gray-800 border-t hover:bg-gray-200"
                                            >GitHub Repository</a
                                        >
                                    </div>
                                </div>
                            </div>
                        </div>
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
import MapContainer from "./map-components/MapContainer";
import LeftContainer from "./LeftContainer";
import RightContainer from "./RightContainer";
import { mapGetters } from "vuex";
import LoadingScreen from "./functional-components/LoadingScreen.vue";

export default {
    name: "BaseContainer",
    components: {
        MapContainer,
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
            dropdownInfo: false,
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
