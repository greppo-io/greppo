<template>
    <div class="h-full w-full">
        <!-- The map container will have the map components and the mail control of the application. -->
        <l-map ref="lmap" :center="center" :zoom="zoom" :maxZoom="25">
            <base-layer v-if="getComponentStatus.baseLayer" />
            <div v-if="getComponentStatus.tileLayer">
                <tile-layer
                    v-for="tileData in getTileLayerData"
                    :key="tileData.id"
                    :layerData="tileData"
                />
            </div>
            <div v-if="getComponentStatus.wmstileLayer">
                <wms-tile-layer
                    v-for="wmstileData in getWMSTileLayerData"
                    :key="wmstileData.id"
                    :layerData="wmstileData"
                />
            </div>
            <div v-if="getComponentStatus.vectorLayer">
                <vector-layer
                    v-for="vectorData in getVectorLayerData"
                    :key="vectorData.id"
                    :layerData="vectorData"
                />
            </div>
            <div v-if="getComponentStatus.imageLayer">
                <image-layer
                    v-for="imageData in getImageLayerData"
                    :key="imageData.id"
                    :imageData="imageData"
                />
            </div>
            <l-control-layers :collapsed="false" v-if="false" />
            <l-control class="leaflet-bar" position="topleft">
                <a
                    class="control-icon"
                    role="button"
                    title="Reset view"
                    @click="resetViewHandler"
                >
                    <unicon
                        name="estate"
                        fill="black"
                        width="22px"
                        height="22px"
                        class="align-middle"
                    ></unicon>
                </a>
            </l-control>
            <draw-feature v-if="getComponentStatus.drawFeature" />
        </l-map>
    </div>
</template>

<script>
import { LMap, LControlLayers, LControl } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import VectorLayer from "./VectorLayer";
import BaseLayer from "./BaseLayer";
import TileLayer from "./TileLayer";
import WMSTileLayer from "./WMSTileLayer";
import { mapGetters } from "vuex";
import DrawFeature from "./DrawFeature.vue";
import ImageLayer from "./ImageLayer.vue";
import { eventHub } from "src/event-hub";

const average = (array) => array.reduce((a, b) => a + b) / array.length;

export default {
    name: "CenterContainer",
    components: {
        LMap,
        LControlLayers,
        LControl,
        BaseLayer,
        TileLayer,
        VectorLayer,
        DrawFeature,
        ImageLayer,
        "wms-tile-layer": WMSTileLayer,
    },
    data() {
        return {
            zoom: 3,
            center: [0, 0],
            layerData: null,
        };
    },
    methods: {
        resetViewHandler() {
            var b00 = [];
            var b01 = [];
            var b10 = [];
            var b11 = [];
            this.getOverlayLayerInfo.forEach((layer) => {
                if (layer.visible && layer.bounds.length) {
                    b00.push(layer.bounds[0][0]);
                    b01.push(layer.bounds[0][1]);
                    b10.push(layer.bounds[1][0]);
                    b11.push(layer.bounds[1][1]);
                }
            });
            const layerBounds = [
                [average(b00), average(b01)],
                [average(b10), average(b11)],
            ];
            this.$refs.lmap.mapObject.fitBounds(layerBounds);
        },
        resetMapContainerSize() {
            setTimeout(() => this.$refs.lmap.mapObject.invalidateSize(), 10);
        },
    },
    computed: {
        ...mapGetters([
            "getTileLayerData",
            "getWMSTileLayerData",
            "getVectorLayerData",
            "getImageLayerData",
            "getOverlayLayerInfo",
            "getComponentStatus",
        ]),
    },
    mounted() {
        this.$nextTick(() => {
            this.$refs.lmap.mapObject.attributionControl.setPosition(
                "bottomleft"
            );        
            if (this.getOverlayLayerInfo.length) {
                this.resetViewHandler();
            }
        });
    },
    created() {
        eventHub.$on("fitOverlayBounds", (layerBounds) => {
            this.$refs.lmap.mapObject.fitBounds(layerBounds);
        });

        eventHub.$on("resetMapContainerSize", () => {
            setTimeout(() => this.$refs.lmap.mapObject.invalidateSize(), 10);
        });
    },
};
</script>

<style>
.leaflet-top {
    margin-top: 4rem;
}
.leaflet-touch .leaflet-control-layers,
.leaflet-touch .leaflet-bar {
    border: none !important;
    background-clip: none !important;
    /* offset-x | offset-y | blur-radius | spread-radius | color */
    box-shadow: 0px 0px 3px 1.5px rgba(0, 0, 0, 0.2) !important;
}
.leaflet-control-attribution {
    font-size: 12px !important;
    letter-spacing: 0.03em;
    font-weight: 400;
    padding: 3px 6px;
    border-radius: 0 4px 0 0;
    color: #666666;
}
.control-icon {
    width: 30px;
    height: 30px;
}
</style>
