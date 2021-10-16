<template>
    <div style="display: none;"></div>
</template>

<script>
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";
import { mapActions } from "vuex";

export default {
    name: "DrawFeature",
    props: {
        defaultDrawFeature: Object,
    },
    methods: {
        ...mapActions([
            "addDrawnFeature",
            "editDrawnFeatures",
            "deleteDrawnFeatures",
            "setDrawFeatureMutation",
        ]),
    },
    mounted: function() {
        this.$nextTick(function() {
            const map = this.$parent.$parent.$refs.lmap.mapObject;

            // Initialise the FeatureGroup to store drawn features
            var drawnFeatures = new window.L.FeatureGroup();
            map.addLayer(drawnFeatures);

            window.L.Edit.Poly = window.L.Edit.Poly.extend({
                options: {
                    icon: new window.L.DivIcon({
                        iconSize: new window.L.Point(10, 10),
                        className:
                            "leaflet-div-icon leaflet-editing-icon my-own-icon",
                    }),
                },
            });

            // define custom marker
            var MyCustomMarker = window.L.Icon.extend({
                options: {
                    shadowUrl: null,
                    iconAnchor: [12, 24],
                    iconSize: [24, 24],
                    iconUrl: require("../../assets/marker.svg"),
                },
            });

            var drawControlOptions = {
                position: "topleft",
                draw: {
                    polyline: {
                        allowIntersection: false,
                        showArea: true,
                        shapeOptions: {
                            color: "#333333",
                            weight: 3,
                        },
                    },
                    polygon: {
                        allowIntersection: false, // Restricts shapes to simple polygons
                        drawError: {
                            color: "#e1e100", // Color the shape will turn when intersects
                            message:
                                "<strong>Polygon draw does not allow intersections!<strong> (allowIntersection: false)", // Message that will show when intersect
                        },
                        shapeOptions: {
                            color: "#333333",
                            weight: 3,
                        },
                    },
                    // Enable only LineString, Polygon, Point now. Circles are not standard format for GIS.
                    circle: false,
                    rectangle: false,
                    marker: {
                        icon: new MyCustomMarker(),
                    },
                    circlemarker: false,
                },
                edit: {
                    featureGroup: drawnFeatures, //REQUIRED!!
                    remove: true,
                    edit: true,
                },
            };

            // Initialise the draw control and pass it the FeatureGroup of editable layers
            var drawControl = new window.L.Control.Draw(drawControlOptions);
            map.addControl(drawControl);

            var markerIcon = window.L.icon({
                shadowUrl: null,
                iconAnchor: [12, 24],
                iconSize: [24, 24],
                iconUrl: require("../../assets/marker.svg"),
            });
            // Handles the draw features sent as default/inputs from the backend
            this.defaultDrawFeature.features.forEach((defaultFeature) => {
                var latlngs = [],
                    _type = defaultFeature.type,
                    layer = {};

                defaultFeature.latlngs.forEach((ll) => {
                    latlngs.push([ll.lat, ll.lng]);
                });

                if (_type == "Polygon") {
                    layer = window.L.polygon(latlngs);
                }

                if (_type == "LineString") {
                    layer = window.L.polyline(latlngs);
                }

                if (_type == "Point") {
                    layer = window.L.marker(latlngs[0], { icon: markerIcon });
                }

                const newFeature = {
                    id: window.L.stamp(layer),
                    type: _type,
                    latlngs: defaultFeature.latlngs,
                };

                drawnFeatures.addLayer(layer);
                this.addDrawnFeature(newFeature);
            });

            // Events to handle draw on the map
            map.on("draw:created", (e) => {
                var type = e.layerType,
                    layer = e.layer,
                    latlngs = [],
                    _type = "";                

                if (type == "polygon") {
                    _type = "Polygon";
                    layer._latlngs[0].forEach((element) => {
                        latlngs.push({ lat: element.lat, lng: element.lng });
                    });
                }
                if (type == "polyline") {
                    _type = "LineString";
                    layer._latlngs.forEach((element) => {
                        latlngs.push({ lat: element.lat, lng: element.lng });
                    });
                }
                if (type == "marker") {
                    _type = "Point";
                    latlngs.push({
                        lat: layer._latlng.lat,
                        lng: layer._latlng.lng,
                    });
                }
                const newFeature = {
                    id: window.L.stamp(layer),
                    type: _type,
                    latlngs: latlngs,
                };

                // update the features drawn to vuex state.
                drawnFeatures.addLayer(layer);
                this.addDrawnFeature(newFeature);
                this.setDrawFeatureMutation(true);
            });

            map.on("draw:edited", (e) => {
                var editLayers = e.layers._layers,
                    editFeatures = [];

                Object.keys(editLayers).forEach((key) => {
                    var layer = editLayers[key];
                    var latlngs = [];

                    if (layer._latlngs) {
                        if (layer._latlngs.length > 1) {
                            layer._latlngs.forEach((element) => {
                                latlngs.push({
                                    lat: element.lat,
                                    lng: element.lng,
                                });
                            });
                        }
                        if (layer._latlngs.length == 1) {
                            layer._latlngs[0].forEach((element) => {
                                latlngs.push({
                                    lat: element.lat,
                                    lng: element.lng,
                                });
                            });
                        }
                    }
                    if (layer._latlng) {
                        latlngs.push({
                            lat: layer._latlng.lat,
                            lng: layer._latlng.lng,
                        });
                    }
                    editFeatures.push({
                        id: window.L.stamp(layer),
                        latlngs: latlngs,
                    });
                });

                // update the features drawn to vuex state.
                this.editDrawnFeatures(editFeatures);
                this.setDrawFeatureMutation(true);
            });

            map.on("draw:deleted", (e) => {
                var deleteLayers = e.layers._layers,
                    deleteFeatures = [];

                Object.keys(deleteLayers).forEach((key) => {
                    var layer = deleteLayers[key];
                    var latlngs = [];

                    if (layer._latlngs) {
                        if (layer._latlngs.length > 1) {
                            layer._latlngs.forEach((element) => {
                                latlngs.push({
                                    lat: element.lat,
                                    lng: element.lng,
                                });
                            });
                        }
                        if (layer._latlngs.length == 1) {
                            layer._latlngs[0].forEach((element) => {
                                latlngs.push({
                                    lat: element.lat,
                                    lng: element.lng,
                                });
                            });
                        }
                    }
                    if (layer._latlng) {
                        latlngs.push({
                            lat: layer._latlng.lat,
                            lng: layer._latlng.lng,
                        });
                    }
                    deleteFeatures.push({
                        id: window.L.stamp(layer),
                        latlngs: latlngs,
                    });
                });

                // update the features drawn to vuex state.
                this.deleteDrawnFeatures(deleteFeatures);
                this.setDrawFeatureMutation(true);
            });
        });
    },
};
</script>

<style scoped>
/* .leaflet-container a {
    color: #FFFFFF !important;
} */
</style>
