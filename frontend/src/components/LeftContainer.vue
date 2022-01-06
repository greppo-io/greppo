<template>
    <div class="flex relative">
        <div
            class="flex flex-col h-screen sidebar sidebar-width"
            v-show="leftContainerOpen"
        >
            <div class="bg-white flex justify-between p-3">
                <div>
                    <button
                        class="focus:outline-none bg-red-600 hover:bg-red-500 rounded text-white px-4 py-1.5 text-xs cursor-pointer"
                        v-if="getInputMutation"
                        @click="postAPI"
                    >
                        reevaluate
                    </button>

                    <button
                        class="focus:outline-none bg-gray-200 rounded text-gray-400 px-4 py-1.5 text-xs cursor-not-allowed"
                        v-if="!getInputMutation"
                        disabled
                    >
                        reevaluate
                    </button>
                </div>

                <div>
                    <button
                        class="focus:outline-none bg-gray-100 hover:bg-gray-200 rounded"
                        @click="toggleAppInfoModal"
                    >
                        <unicon
                            name="info-circle"
                            fill="gray"
                            class="pt-1 px-1.5"
                            width="20px"
                        ></unicon>
                    </button>
                </div>
            </div>

            <!-- Left Side Bar Content  -->
            <div class="relative px-3 bg-white h-full overflow-auto">
                <!-- Implement the switch case for the type of input component.type -->

                <p v-if="getAppInfo.title" class="font-medium text-2xl">{{ getAppInfo.title }}</p>

                <layer-control v-show="true" />

                <draw-feature-control v-if="getComponentStatus.drawFeature" />

                <div
                    v-for="component in getInputComponentInfo"
                    :key="component.id"
                >
                    <input-control :data="component" />
                    <chart-control :data="component" />
                    <display-control :data="component" />
                </div>
            </div>
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
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { eventHub } from "src/event-hub";
import LayerControl from "./map-components/LayerControl";
import InputControl from "./input-components/InputControl.vue";
import ChartControl from "./chart-components/ChartControl.vue";
import DrawFeatureControl from "./map-components/DrawFeatureControl.vue";
import DisplayControl from "./display-components/DisplayControl.vue";

export default {
    name: "LeftContainer",
    data() {
        return {
            leftContainerOpen: true,
        };
    },
    components: {
        LayerControl,
        InputControl,
        ChartControl,
        DrawFeatureControl,
        DisplayControl,
    },
    methods: {
        ...mapActions(["postAPI", "setAppInfo"]),
        toggleLeftContainer() {
            this.leftContainerOpen = !this.leftContainerOpen;
            if (this.getComponentStatus.mapComponent) {
                eventHub.$emit("resetMapContainerSize");
            }
        },
        toggleAppInfoModal() {
            this.setAppInfo({ modal: true });
        },
    },
    computed: mapGetters([
        "getInputComponentInfo",
        "getComponentStatus",
        "getInputMutation",
        "getAppInfo",
    ]),
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
