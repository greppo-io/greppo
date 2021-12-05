<template>
    <div
        v-if="getComponentStatus.baseLayer || getComponentStatus.overlayLayer"
        class="block my-5 border-2 rounded"
        :class="collapse ? 'border-white' : 'border-gray-100'"
    >
        <div
            class="flex flex-row justify-between items-center cursor-pointer bg-gray-100 rounded px-3 py-3 transition-all duration-500"
            @click="collapse = !collapse"
        >
            <p>Layer control</p>
            <span
                :class="collapse ? 'rotate-0' : 'rotate-180'"
                class="fill-current h-6 w-6 transform transition-transform duration-500"
            >
                <unicon name="angle-down" fill="black"></unicon>
            </span>
        </div>
        <div
            :class="collapse ? 'max-h-0' : 'max-h-96'"
            class="overflow-hidden transition-all duration-500 pl-5 pt-2 pr-2"
        >
            <div
                :class="
                    getComponentStatus.baseLayer &&
                    getComponentStatus.overlayLayer
                        ? 'mb-5'
                        : 'mb-3'
                "
                v-if="getComponentStatus.baseLayer"
            >
                <label class="block">
                    <span class="text-gray-700">Base layer control</span>
                    <base-layer-control />
                </label>
            </div>
            <div v-if="getComponentStatus.overlayLayer">
                <div class="block overflow-auto max-h-72">
                    <span class="text-gray-700">Overlay layer control</span>
                    <overlay-layer-control
                        v-for="vector in getOverlayLayerInfo"
                        :key="vector.id"
                        :layerData="vector"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import OverlayLayerControl from "./OverlayLayerControl.vue";
import { mapGetters } from "vuex";
import BaseLayerControl from "./BaseLayerControl.vue";

export default {
    name: "LayerControl",
    components: {
        OverlayLayerControl,
        BaseLayerControl,
    },
    data() {
        return {
            collapse: false,
        };
    },
    computed: {
        ...mapGetters(["getOverlayLayerInfo", "getComponentStatus"]),
    },
};
</script>

<style></style>
