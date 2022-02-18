<template>
    <l-wms-tile-layer
        :base-url="layerData.url"
        :layers="layerData.layers[0]"
        :visible="layerData.visible"
        :opacity="layerData.opacity"
        :subdomains="layerData.subdomains"
        :name="layerData.name"
        :attribution="layerData.attribution[0]"
        :transparent="layerData.transparent[0]"
        :format="layerData.format[0]"
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
