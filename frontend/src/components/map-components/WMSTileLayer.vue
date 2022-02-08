<template>
    <l-wms-tile-layer
        :base-url="layerData.url"
        :layers="layerData.layers"
        :visible="layerData.visible"
        :opacity="layerData.opacity"
        :subdomains="layerData.subdomains"
        :name="layerData.name"
        :attribution="layerData.attribution"
        :transparent="layerData.transparent"
        :format="layerData.format"
        layer-type="overlay"
    >
    </l-wms-tile-layer>
</template>

<script>
import { LWMSTileLayer } from "vue2-leaflet";
import { mapGetters } from "vuex";
export default {
    name: "WMSTileLayer",
    props: {
        layerData: Object,
    },
    components: {
        "l-wms-tile-layer": LWMSTileLayer,
    },
    computed: {
        ...mapGetters(["getLayerVisibility"]),
    },
};
</script>

<style></style>
