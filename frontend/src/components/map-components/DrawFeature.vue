<template>
    <div style="display: none;"></div>
</template>

<script>
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";
import { mapActions, mapGetters } from "vuex";
import { eventHub } from "src/event-hub";

export default {
    name: "DrawFeature",    
    data() {
        return {
            featureGroup: null,
            mapObject: null,
            activeDrawFeatureID: null,
            activeGeometry: [],
            drawControl: null,
        };
    },
    methods: {
        ...mapActions([
            "setDrawFeatureDrawn",
            "addDrawFeature",
            "editDrawFeature",
            "deleteDrawFeature",
        ]),
        toggleDrawTools() {
            // If control already exists, remove it
            if (this.drawControl)
                this.mapObject.removeControl(this.drawControl);

            // Define custom marker TODO 
            var customMarker = window.L.Icon.extend({
                options: {
                    shadowUrl: null,
                    iconAnchor: [12, 24],
                    iconSize: [24, 24],
                    iconUrl: require("../../assets/marker.svg"),
                },
            });

            var _pointOptions = this.activeGeometry.includes("Point")
                ? {
                      icon: new customMarker(),
                  }
                : false;
            var _polylineOptions = this.activeGeometry.includes("LineString")
                ? {
                      allowIntersection: false,
                      showArea: true,
                      shapeOptions: {
                          color: "#333333",
                          weight: 3,
                      },
                  }
                : false;
            var _polygonOptions = this.activeGeometry.includes("Polygon")
                ? {
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
                  }
                : false;

            var drawControlOptions = {
                position: "topleft",
                draw: {
                    polyline: _polylineOptions,
                    polygon: _polygonOptions,
                    // Enable only LineString, Polygon, Point now. Circles are not standard format for GIS.
                    circle: false,
                    rectangle: false,
                    marker: _pointOptions,
                    circlemarker: false,
                },
                edit: {
                    featureGroup: this.featureGroup,
                    remove: true,
                    edit: true,
                },
            };

            // Initialise the draw control and pass it the FeatureGroup of editable layers
            var drawControl = new window.L.Control.Draw(drawControlOptions);
            this.mapObject.addControl(drawControl);
            this.drawControl = drawControl;
        },
        mountActiveDrawFeature() {
            const DrawFeatureData = this.getDrawFeatureData;
            const drawFeatureIndex = DrawFeatureData.findIndex(
                (drawFeature) => drawFeature.active === true
            );
            if (drawFeatureIndex !== -1) {
                this.activeDrawFeatureID = DrawFeatureData[drawFeatureIndex].id;
                this.activeGeometry =
                    DrawFeatureData[drawFeatureIndex].geometry;
                this.toggleDrawTools();
                this.featureGroup.clearLayers();
                DrawFeatureData[drawFeatureIndex].featuresDrawn.forEach(
                    (feature) => {
                        this.featureGroup.addLayer(feature.layer);
                    }
                );
            } else {
                console.log("Log error, DrawFeature.vue");
            }
        },
        initializeDrawFeatureDrawn() {
            var markerIcon = window.L.icon({
                shadowUrl: null,
                iconAnchor: [12, 24],
                iconSize: [24, 24],
                iconUrl: require("../../assets/marker.svg"),
            });

            // Loops through the deafult feature data passed in, and initializess
            // them to latlng in state.DrawFeatureData
            var initialFeaturesDrawnData = [];
            const DrawFeatureData = this.getDrawFeatureData;
            DrawFeatureData.forEach((drawFeature) => {
                var featuresDrawn = [];
                drawFeature.features.forEach((defaultFeature) => {
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
                        layer = window.L.marker(latlngs[0], {
                            icon: markerIcon,
                        });
                    }

                    const newFeature = {
                        id: window.L.stamp(layer),
                        type: _type,
                        latlngs: defaultFeature.latlngs,
                        layer: layer,
                    };

                    featuresDrawn.push(newFeature);
                });
                initialFeaturesDrawnData.push({
                    drawFeatureID: drawFeature.id,
                    featuresDrawn: featuresDrawn,
                });
            });
            this.setDrawFeatureDrawn(initialFeaturesDrawnData);
        },
    },
    computed: {
        ...mapGetters(["getDrawFeatureData"]),
    },
    created() {
        eventHub.$on("changeDrawFeatureLayer", () => {
            this.mountActiveDrawFeature();
        });

        eventHub.$on("reInitializeDrawFeature", () => {
            this.initializeDrawFeatureDrawn();
        });        

        const map = this.$parent.$parent.$refs.lmap.mapObject;
        // Initialise the FeatureGroup to store drawn features
        var featureGroup = new window.L.FeatureGroup();
        map.addLayer(featureGroup);

        this.mapObject = map;
        this.featureGroup = featureGroup;

        // What is this? TODO
        window.L.Edit.Poly = window.L.Edit.Poly.extend({
            options: {
                icon: new window.L.DivIcon({
                    iconSize: new window.L.Point(10, 10),
                    className:
                        "leaflet-div-icon leaflet-editing-icon my-own-icon",
                }),
            },
        });
    },
    mounted: function() {
        this.$nextTick(function() {
            this.initializeDrawFeatureDrawn();
            this.mountActiveDrawFeature();

            // Event to handle new feature drawn on the map
            this.mapObject.on("draw:created", (e) => {
                var type = e.layerType,
                    newLayer = e.layer,
                    latlngs = [],
                    _type = "";

                if (type == "polygon") {
                    _type = "Polygon";
                    newLayer._latlngs[0].forEach((element) => {
                        latlngs.push({ lat: element.lat, lng: element.lng });
                    });
                }
                if (type == "polyline") {
                    _type = "LineString";
                    newLayer._latlngs.forEach((element) => {
                        latlngs.push({ lat: element.lat, lng: element.lng });
                    });
                }
                if (type == "marker") {
                    _type = "Point";
                    latlngs.push({
                        lat: newLayer._latlng.lat,
                        lng: newLayer._latlng.lng,
                    });
                }
                const newFeature = {
                    id: window.L.stamp(newLayer),
                    type: _type,
                    latlngs: latlngs,
                    layer: newLayer,
                };

                // update the features drawn to vuex state.
                this.featureGroup.addLayer(newLayer);
                this.addDrawFeature({
                    newFeature,
                    drawFeatureID: this.activeDrawFeatureID,
                });
            });

            // Event to handle feature edit on the map
            this.mapObject.on("draw:edited", (e) => {
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
                        layer: layer,
                    });
                });

                // update the features drawn to vuex state.
                this.editDrawFeature({
                    editFeatures,
                    drawFeatureID: this.activeDrawFeatureID,
                });
            });

            // Event to handle feature delete on the map
            this.mapObject.on("draw:deleted", (e) => {
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
                this.deleteDrawFeature({
                    deleteFeatures,
                    drawFeatureID: this.activeDrawFeatureID,
                });
            });
        });
    },
};
</script>

<style>
/* .leaflet-container a {
    color: #FFFFFF !important;
} */
</style>
