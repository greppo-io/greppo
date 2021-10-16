<template>
    <div>
        <l-tile-layer
            v-for="layer in getBaseLayerInfo"
            :key="layer.name"
            :name="layer.name"
            :visible="layer.visible"
            :url="layer.url"
            :attribution="layer.attribution"
            layer-type="base"
        ></l-tile-layer>
    </div>
</template>
<script>
import { LTileLayer } from "vue2-leaflet";
import { mapGetters } from "vuex";

export default {
    name: "BaseLayer",
    components: {
        LTileLayer,
    },
    computed: mapGetters(["getBaseLayerInfo"]),
};
</script>
