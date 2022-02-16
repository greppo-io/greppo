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
    methods: {
        getChoroplethColor(d) {
            console.log(this.layerData.style.choropleth.bins);
            const index = this.layerData.style.choropleth.bins.findIndex(
                (item) => d > item
            );
            console.log(index);
            const color = this.layerData.style.choropleth.palette[index];
            return color;
        },
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
            return (feature) => {
                return {
                    stroke: this.layerData.style.stroke || true,
                    color:
                        this.layerData.style.color ||
                        this.layerData.style.fillColor,
                    weight: this.layerData.style.weight || 2,
                    opacity: this.layerData.style.opacity || 1,
                    lineCap: this.layerData.style.lineCap || "round",
                    lineJoin: this.layerData.style.lineJoin || "round",
                    dashArray: this.layerData.style.dashArray || null,
                    dashOffset: this.layerData.style.dashOffset || null,
                    fill: this.layerData.style.fill || true,
                    // fillColor:  this.layerData.style.fillColor,
                    fillColor: this.layerData.style.choropleth
                        ? this.getChoroplethColor(
                              feature.properties[
                                  this.layerData.style.choropleth.key_on
                              ]
                          )
                        : this.layerData.style.fillColor,
                    fillOpacity: this.layerData.style.fillOpacity || 0.8,
                    radius: this.layerData.style.radius || 3,
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
