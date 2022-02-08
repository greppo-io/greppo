<template>
    <l-image-overlay
        :name="imageData.title"
        :url="imageData.url"
        :bounds="imageData.bounds"
        :visible="getLayerVisibility.bind(this, imageData.id)()"
        layer-type="overlay"
    />
</template>

<script>
import { LImageOverlay } from "vue2-leaflet";
import { mapGetters } from "vuex";

export default {
    name: "ImageLayer",
    components: {
        LImageOverlay,
    },
    props: {
        imageData: Object,
    },
    computed: {
        ...mapGetters(["getLayerVisibility"]),
    },
};
</script>

<style></style>
