<template>
    <l-geo-json
        :name="layerData.name"
        :geojson="layerData.data"
        :options="options"
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
    computed: {
        ...mapGetters(["getLayerVisibility"]),
        options() {
            return {
                onEachFeature: this.onEachFeatureFunction,
                pointToLayer: this.pointToLayerFunction,
                style: this.styleFunction,
            };
        },
        pointToLayerFunction() {
            return (feature, latlng) => {
                return window.L.circleMarker(latlng);
            };
        },
        styleFunction() {
            return () => {
                return {
                    color: this.layerData.style.fillColor,
                    opacity: 1,
                    weight: 2,
                    fillColor: this.layerData.style.fillColor,
                    fillOpacity: 0.7,
                    radius: 3,
                };
            };
        },
        onEachFeatureFunction() {
            return (feature, layer) => {
                if (feature.properties) {
                    var bindContent = "<div>";
                    for (var p in feature.properties) {
                        bindContent +=
                            '<p style="margin: 5px 10px;"><span style="font-weight:500;">' +
                            p +
                            "</span>:  " +
                            feature.properties[p] +
                            "</p>";
                    }
                    bindContent += "</div>";
                    // Bind a popup
                    // layer.bindPopup(bindContent);                    
                    // Bind a tooltip
                    layer.bindTooltip(bindContent, {
                        permanent: false,
                        sticky: true,
                    });
                }
            };
        },
    },
};
</script>

<style></style>
