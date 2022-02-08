<template>
    <l-tile-layer
        :name="layerData.name"
        :url="layerData.url"
        :opcaity="layerData.opcaity"
        :subdomains="layerData.subdomains"
        :visible="getLayerVisibility.bind(this, layerData.id)()"
        layer-type="overlay"
    >
    </l-tile-layer>
</template>

<script>
import { LTileLayer } from "vue2-leaflet";
import { mapGetters } from "vuex";
export default {
    name: "TileLayer",
    props: {
        layerData: Object,
    },
    components: {
        LTileLayer,
    },
    computed: {
        ...mapGetters(["getLayerVisibility"]),
    },
};
</script>

<style></style>
