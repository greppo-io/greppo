<template>
    <div class="h-full w-full">        
        <!-- The center container will have the map components and the mail control of the application. -->
        <l-map ref="lmap" :center="center" :zoom="zoom">
            <base-layer v-if="getComponentStatus.baseLayer" />
            <div v-if="getComponentStatus.overlayLayer">
                <vector-layer
                    v-for="vectorData in getVectorData"
                    :key="vectorData.id"
                    :layerData="vectorData"
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
            <l-control class="leaflet-bar" position="topleft">
                <a
                    class="control-icon"
                    role="button"
                    title="Full-screen toggle"
                    @click="$emit('toggle-fullscreen', isFullScreen)"
                >
                    <unicon
                        v-show="!isFullScreen"
                        name="expand-arrows-alt"
                        fill="black"
                        width="19px"
                        height="19px"
                        class="align-middle"
                    ></unicon>
                    <unicon
                        v-show="isFullScreen"
                        name="compress-arrows"
                        fill="black"
                        width="19px"
                        height="19px"
                        class="align-middle"
                    ></unicon>
                </a>
            </l-control>
            <draw-feature
                v-if="getDrawFeatureState"
                :defaultDrawFeature="getDefaultDrawFeatures"
            />
        </l-map>
    </div>
</template>

<script>
import { LMap, LControlLayers, LControl } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import VectorLayer from "./map-components/VectorLayer";
import BaseLayer from "./map-components/BaseLayer";
import { mapGetters } from "vuex";
import DrawFeature from "./map-components/DrawFeature.vue";

export default {
    name: "CenterContainer",
    components: {
        LMap,
        LControlLayers,
        LControl,
        BaseLayer,
        VectorLayer,
        DrawFeature,
    },
    props: {
        isFullScreen: Boolean,
    },
    data() {
        return {
            zoom: 3,
            center: [0, 0],
            layerData: null,
            viewzoom: null,
        };
    },
    methods: {
        resetViewHandler() {
            this.viewzoom = this.getViewZoom;
            this.$refs.lmap.mapObject.setView(
                [this.viewzoom[0], this.viewzoom[1]],
                this.viewzoom[2]
            );
        },
        resetMapContainerSize() {
            setTimeout(() => this.$refs.lmap.mapObject.invalidateSize(), 10);
        },
    },
    computed: {
        ...mapGetters([
            "getVectorData",
            "getViewZoom",
            "getDrawFeatureState",
            "getDefaultDrawFeatures",
            "getComponentStatus",
        ]),
    },   
    // mounted() {
    //     this.$nextTick(() => {
    //         this.$refs.lmap.mapObject.attributionControl
    //             .setPosition('bottomleft');
    //     });
    // }, 
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
    border-radius: 4px 0 0 0;
    color: #666666;
}
.control-icon {
    width: 30px;
    height: 30px;
}
</style>
