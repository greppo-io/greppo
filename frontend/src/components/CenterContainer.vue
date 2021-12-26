<template>
    <div class="flex flex-col w-full h-screen">
        <div class="h-full relative">
            <!-- Center Container Content  -->
            <map-container
                v-if="getComponentStatus.mapComponent"
                :isFullScreen="isFullScreen"
                @toggle-fullscreen="toggleFullScreen"
            />

            <div
                class="absolute top-2 right-16 bg-white bg-opacity-70 rounded-md px-2 py-1"
                style="z-index: 1500;"
                v-if="getStatus === 1"
            >
                <div class="flex flex-row items-center">
                    <div class="text-center text-gray-700">
                        <div class="flex flex-row mt-1 p-0.5 items-center">
                            <div class="flex justify-center items-center">
                                <div
                                    class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-red-600"
                                ></div>
                                <div
                                    class="animate-ping absolute inline-flex h-12 w-12 rounded-full bg-red-400 opacity-75"
                                ></div>
                            </div>
                            <p class="text-sm ml-2">Evaluating !</p>
                        </div>
                    </div>
                </div>
            </div>

            <div
                class="absolute top-2 right-2 bg-white bg-opacity-70 rounded-md"
                style="z-index: 1500;"
            >
                <div class="flex flex-row items-center">
                    <button
                        class="flex items-end relative hover:bg-gray-200 rounded px-1 py-0.5"
                        @click="dropdownInfo = !dropdownInfo"
                    >
                        <unicon
                            name="sort-amount-down"
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
                        class="absolute top-12 right-0 w-48 bg-white bg-opacity-70 rounded-md overflow-hidden shadow-lg z-20"
                    >
                        <button
                            @click="toggleAppInfoModal"
                            class="block px-4 py-3 font-medium text-gray-800 border-b"
                        >
                            About me
                        </button>
                        <a
                            href="https://github.com/greppo-io/greppo"
                            target="_blank"
                            class="block px-4 py-3 text-sm text-gray-800 hover:bg-gray-200"
                            >Made with Greppo</a
                        >
                        <a
                            href="https://docs.greppo.io/"
                            target="_blank"
                            class="block px-4 py-3 text-sm text-gray-800 hover:bg-gray-200"
                            >Greppo docs</a
                        >
                        <a
                            href="https://greppo.io/"
                            target="_blank"
                            class="block px-4 py-3 text-sm text-gray-800 border-t hover:bg-gray-200"
                            >greppo.io</a
                        >
                    </div>
                </div>
            </div>

            <div
                class="absolute bottom-0 right-2 bg-white bg-opacity-70 rounded-t-md px-2 pt-1 pb-2"
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
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import MapContainer from "./map-components/MapContainer";
import { mapGetters, mapActions } from "vuex";

export default {
    name: "CenterContainer",
    components: {
        MapContainer,
    },
    data() {
        return {
            dropdownInfo: false,
        };
    },
    methods: {
        ...mapActions(["setAppInfo"]),
        toggleAppInfoModal() {
            this.dropdownInfo = !this.dropdownInfo;
            this.setAppInfo({ modal: true });
        },
    },
    computed: {
        ...mapGetters(["getStatus", "getComponentStatus"]),
    },
};
</script>

<style></style>
