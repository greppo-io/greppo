<template>
    <l-geo-json
        :geojson="layerData.data"
        :options="options"
        :options-style="styleFunction"
        :name="layerData.title"
        :visible="getLayerVisibility.bind(this, layerData.id)()"
        layer-type="overlay"
    ></l-geo-json>
</template>

<script>
import { LGeoJson } from "vue2-leaflet";
import { mapGetters } from "vuex";

export default {
    name: "VectorLayer",
    props: {
        layerData: Object,
    },
    components: {
        LGeoJson,
    },
    data() {
        return {
            style: null,
        };
    },
    computed: {
        ...mapGetters(["getLayerVisibility"]),
        options() {
            return {
                onEachFeature: this.onEachFeatureFunction,
            };
        },
        styleFunction() {
            const fillColor = this.style.fillColor; // important! need touch fillColor in computed for re-calculate when change fillColor
            return () => {
                return {
                    weight: 2,
                    color: fillColor,
                    opacity: 1,
                    fillColor: fillColor,
                    fillOpacity: 0.7,
                };
            };
        },
        onEachFeatureFunction() {
            return (feature, layer) => {
                if (feature.properties) {
                    var popupContent = "<div>";
                    for (var p in feature.properties) {
                        popupContent +=
                            '<p style="margin: 5px 0px;"><span style="font-weight:600;">' +
                            p +
                            "</span>: " +
                            feature.properties[p] +
                            "</p>";
                    }
                    popupContent += "</div>";
                    layer.bindPopup(popupContent);
                }
            };
        },
    },
    async created() {        
        this.style = this.layerData.style;
    },
};
</script>

<style></style>
