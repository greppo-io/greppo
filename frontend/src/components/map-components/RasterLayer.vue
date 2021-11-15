<template>
    <l-image-overlay
        :name="rasterData.title"
        :url="rasterData.url"
        :bounds="rasterData.bounds"
        :visible="getLayerVisibility.bind(this, rasterData.id)()"
        layer-type="overlay"
    />
</template>

<script>
import { LImageOverlay } from "vue2-leaflet";
import { mapGetters } from "vuex";

export default {
    name: "RasterLayer",
    components: {
        LImageOverlay,
    },
    props: {
        rasterData: Object,
    },
    data() {
        return {
            // imageUrl:
            //     "http://127.0.0.1:8000/raster",
            // imageBounds: [
            //     [52.32145194544034, 4.885192279157401],
            //     [52.35012299897077, 4.899747081326474],
            // ],
        };
    },
    computed: {
        ...mapGetters(["getLayerVisibility"]),
    },
};
</script>

<style></style>
