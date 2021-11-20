import axios from "axios";
import { eventHub } from "src/event-hub";

const average = (array) => array.reduce((a, b) => a + b) / array.length;

// Status codes
// 1: Created application
// 2: Fetch data finished
// 3: Draw visualization

const state = {
    Status: 1,
    ComponentStatus: {
        baseLayer: false,
        overlayLayer: false,
        rasterLayer: false,
        mapComponent: false,
        inputComponent: false,
        drawFeature: false,
    },
    VectorData: null,
    BaseLayerInfo: null,
    OverlayLayerInfo: null,
    ViewZoom: [0, 0, 3],
    ChartEventData: null,
    InputComponentInfo: null,
    DrawFeatureData: {
        id: "draw-feature-id",
        name: "Default features",
        features: [],
        mutation: false,
        active: false,
        featuresDrawn: [],
    },
    InputMutation: false,
    RasterData: null,
    RasterLayerInfo: null,
};

const getters = {
    getStatus: (state) => state.Status,
    getComponentStatus: (state) => state.ComponentStatus,
    getVectorData: (state) => state.VectorData,
    getBaseLayerInfo: (state) => state.BaseLayerInfo,
    getOverlayLayerInfo: (state) => state.OverlayLayerInfo,
    getViewZoom: (state) => state.ViewZoom,
    getChartEventData: (state) => state.ChartEventData,
    getLayerVisibility: (state) => (id) => {
        // To obtain the visibility of the specific layer passed as argument.
        return state.OverlayLayerInfo.find((element) => element.id == id)
            .visible;
    },
    getInputComponentInfo: (state) => state.InputComponentInfo,
    getInputComponentData: (state) => (id) => {
        return state.InputComponentInfo.find((element) => element.id == id);
    },
    getInputMutation: (state) => state.InputMutation,
    getDrawFeatureData: (state) => state.DrawFeatureData,
    getRasterData: (state) => state.RasterData,
    getRasterLayerInfo: (state) => state.RasterLayerInfo,
};

const actions = {
    async getAPI({ commit, dispatch }) {
        try {
            const response = await axios.get(process.env.VUE_APP_API);
            dispatch("commitResponseData", response);
            commit("commitStatus", 2);
        } catch (error) {
            // TODO Frontend error logging
            console.log("Error in getting data.", error);
        }
    },

    async postAPI({ commit, state, dispatch }) {
        var postData = {};
        state.InputComponentInfo.forEach((component) => {
            if (component.mutate) {
                if (component.type == "Number") {
                    postData[component.name] = Number(component.value);
                } else {
                    postData[component.name] = component.value;
                }
            }
        });

        // TODO change this to the new post draw feature
        // if (state.draw-feature.mutation) {
        //     postData[state.draw-feature.name] = state.draw-feature;
        // }
        function mapDrawFeature(feature) {
            return {
                id: feature.id,
                type: feature.type,
                latlngs: feature.latlngs,
            };
        }

        state.DrawFeatureData.forEach((drawFeature) => {
            if (drawFeature.mutation) {
                postData[drawFeature.name] = drawFeature.featuresDrawn.map(
                    mapDrawFeature
                );
            }
        });

        axios
            .post(process.env.VUE_APP_API, postData)
            .then(function(response) {
                dispatch("commitResponseData", response);
                commit("commitInputMutation", false);
                eventHub.$emit("reInitializeDrawFeature");
            })
            .catch(function(error) {
                // TODO Frontend error logging
                console.log("Error in posting data.", error);
            });
    },

    commitResponseData({ commit, state }, response) {
        var ComponentStatus = state.ComponentStatus;        

        const responseBaseLayerInfo = response.data.base_layer_info;
        const responseVectorData = response.data.overlay_layer_data;
        const responseComponentInfo = response.data.component_info;
        const responseRasterData = response.data.raster_layer_data;
        var overlayLayerInfo = [];

        if (responseBaseLayerInfo.length) {
            ComponentStatus.baseLayer = true;
            commit("commitBaseLayerInfo", responseBaseLayerInfo);
        }
        
        // const responseRasterData = [        
        //     {
        //         id: "1qaz",
        //         title: "raster 1",
        //         description: "description raster 1",
        //         url: "http://www.lib.utexas.edu/maps/historical/newark_nj_1922.jpg",                
        //         bounds: [
        //             [40.712216, -74.22655],
        //             [40.773941, -74.12544],
        //         ],
        //         visible: true,
        //     },
        // ];

        if (responseRasterData.length) {
            ComponentStatus.rasterLayer = true;
            commit("commitRasterData", responseRasterData);

            responseRasterData.forEach(function(layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    title: layerData.title,
                    description: layerData.description,
                    visible: layerData.visible,
                    color: "#123123",
                    type: "raster",
                });
            });
        }

        if (responseVectorData.length) {
            ComponentStatus.overlayLayer = true;
            commit("commitVectorData", responseVectorData);

            let viewzoomInfo = [];
            responseVectorData.forEach(function(layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    title: layerData.title,
                    description: layerData.description,
                    visible: layerData.visible,
                    color: layerData.style.fillColor,
                    type: "vector",
                });
                viewzoomInfo.push({
                    id: layerData.id,
                    viewzoom: layerData.viewzoom,
                });
            });

            // Commit zoom and view, 1st step just average the x,y and min of zoom.
            // TODO Next based on the visible layers.
            const viewzoom = [
                average(viewzoomInfo.map((a) => a.viewzoom[0])),
                average(viewzoomInfo.map((a) => a.viewzoom[1])),
                Math.min(...viewzoomInfo.map((a) => a.viewzoom[2])),
            ];
            commit("commitViewZoom", viewzoom);
        }

        commit("commitOverlayLayerInfo", overlayLayerInfo);

        if (responseComponentInfo.length) {
            ComponentStatus.inputComponent = true;

            commit("commitInputComponentInfo", responseComponentInfo);

            var DrawFeatureData = [];
            var activateDrawFeature = true;
            responseComponentInfo.forEach((component) => {
                if (component.type === "DrawFeature") {
                    DrawFeatureData.push({
                        id: component.id,
                        name: component.name,
                        geometry: component.geometry,
                        features: component.features,
                        mutation: false,
                        active: activateDrawFeature,
                        featuresDrawn: [],
                    });
                    if (activateDrawFeature) {
                        activateDrawFeature = !activateDrawFeature;
                    }
                }
            });
            if (DrawFeatureData.length) {
                ComponentStatus.drawFeature = true;
                commit("commitDrawFeatureData", DrawFeatureData);
            }
        }

        if (
            ComponentStatus.baseLayer ||
            ComponentStatus.overlayLayer ||
            ComponentStatus.drawFeature
        ) {
            ComponentStatus.mapComponent = true;
        }

        commit("commitComponentStatus", ComponentStatus);
    },

    setBaseLayerVisibility({ commit }, data) {
        commit("updateBaseLayerVisibility", data);
    },

    setOverlayLayerVisibility({ commit }, data) {
        commit("updateOverlayLayerVisibility", data);
    },

    setChartEventData({ commit }, data) {
        commit("commitChartEventData", data);
    },

    setInputComponentData({ commit, state }, data) {
        if (!state.InputMutation) {
            commit("commitInputMutation", true);
        }
        commit("updateInputComponentData", data);
    },

    activateDrawFeatureLayer({ commit, state }, layerName) {
        var DrawFeatureData = state.DrawFeatureData;
        DrawFeatureData.forEach((feature) => {
            if (feature.name == layerName) {
                feature.active = true;
            } else {
                feature.active = false;
            }
        });
        commit("commitDrawFeatureData", DrawFeatureData);
    },

    setDrawFeatureDrawn({ commit, state }, initialFeaturesDrawn) {
        var DrawFeatureData = state.DrawFeatureData;
        initialFeaturesDrawn.forEach((featuresDrawn) => {
            const indexDrawFeature = DrawFeatureData.findIndex(
                (drawFeature) => drawFeature.id === featuresDrawn.drawFeatureID
            );
            if (indexDrawFeature !== -1) {
                DrawFeatureData[indexDrawFeature].featuresDrawn =
                    featuresDrawn.featuresDrawn;
            }
        });
        commit("commitDrawFeatureData", DrawFeatureData);
    },

    addDrawFeature({ commit, state }, { newFeature, drawFeatureID }) {
        var DrawFeatureData = state.DrawFeatureData;
        const indexDrawFeature = DrawFeatureData.findIndex(
            (drawFeature) => drawFeature.id === drawFeatureID
        );
        if (indexDrawFeature !== -1) {
            DrawFeatureData[indexDrawFeature].featuresDrawn.push(newFeature);
            if (!DrawFeatureData[indexDrawFeature].mutation) {
                DrawFeatureData[indexDrawFeature].mutation = true;
            }
            if (!state.InputMutation) {
                commit("commitInputMutation", true);
            }
        }

        commit("commitDrawFeatureData", DrawFeatureData);
    },

    editDrawFeature({ commit, state }, { editFeatures, drawFeatureID }) {
        var DrawFeatureData = state.DrawFeatureData;
        const indexDrawFeature = DrawFeatureData.findIndex(
            (drawFeature) => drawFeature.id === drawFeatureID
        );
        if (indexDrawFeature !== -1) {
            editFeatures.forEach((editFeature) => {
                const featureDrawnIndex = DrawFeatureData[
                    indexDrawFeature
                ].featuresDrawn.findIndex(
                    (featureDrawn) => featureDrawn.id === editFeature.id
                );
                if (featureDrawnIndex !== -1) {
                    DrawFeatureData[indexDrawFeature].featuresDrawn[
                        featureDrawnIndex
                    ].latlngs = editFeature.latlngs;
                    DrawFeatureData[indexDrawFeature].featuresDrawn[
                        featureDrawnIndex
                    ].layer = editFeature.layer;
                }
            });

            if (!DrawFeatureData[indexDrawFeature].mutation) {
                DrawFeatureData[indexDrawFeature].mutation = true;
            }
            if (!state.InputMutation) {
                commit("commitInputMutation", true);
            }
        }
        commit("commitDrawFeatureData", DrawFeatureData);
    },

    deleteDrawFeature({ commit, state }, { deleteFeatures, drawFeatureID }) {
        var DrawFeatureData = state.DrawFeatureData;
        const indexDrawFeature = DrawFeatureData.findIndex(
            (drawFeature) => drawFeature.id === drawFeatureID
        );

        if (indexDrawFeature !== -1) {
            deleteFeatures.forEach((deleteFeature) => {
                const featureDrawnIndex = DrawFeatureData[
                    indexDrawFeature
                ].featuresDrawn.findIndex(
                    (featureDrawn) => featureDrawn.id === deleteFeature.id
                );
                if (featureDrawnIndex !== -1) {
                    DrawFeatureData[indexDrawFeature].featuresDrawn.splice(
                        featureDrawnIndex,
                        1
                    );
                }
            });

            if (!DrawFeatureData[indexDrawFeature].mutation) {
                DrawFeatureData[indexDrawFeature].mutation = true;
            }
            if (!state.InputMutation) {
                commit("commitInputMutation", true);
            }
        }
        commit("commitDrawFeatureData", DrawFeatureData);
    },
};

const mutations = {
    commitStatus: (state, data) => {
        state.Status = data;
    },
    commitComponentStatus: (state, data) => {
        state.ComponentStatus = data;
    },
    commitVectorData: (state, data) => {
        state.VectorData = data;
    },
    commitBaseLayerInfo: (state, data) => {
        state.BaseLayerInfo = data;
    },
    commitOverlayLayerInfo: (state, data) => {
        state.OverlayLayerInfo = data;
    },
    commitInputMutation: (state, data) => {
        state.InputMutation = data;
    },
    commitViewZoom: (state, data) => {
        state.ViewZoom = data;
    },
    commitChartEventData: (state, data) => {
        state.ChartEventData = data;
    },
    updateOverlayLayerVisibility: (state, layerVisibility) => {
        const index = state.OverlayLayerInfo.findIndex(
            (layer) => layer.id === layerVisibility.id
        );
        if (index !== -1) {
            state.OverlayLayerInfo[index].visible = layerVisibility.visible;
        }
    },
    updateBaseLayerVisibility: (state, layerID) => {
        state.BaseLayerInfo.forEach((layer) => {
            if (layer.id == layerID) {
                layer.visible = true;
            } else {
                layer.visible = false;
            }
        });
    },
    updateInputComponentData: (state, componentData) => {
        state.InputComponentInfo.forEach((inputComponent) => {
            if (inputComponent.id == componentData.id) {
                if (!inputComponent.mutate) {
                    inputComponent.mutate = true;
                    inputComponent.oldValue = inputComponent.value;
                }
                inputComponent.value = componentData.value;
            }
        });
    },
    commitInputComponentInfo: (state, data) => {
        state.InputComponentInfo = data;
    },
    commitDrawFeatureData: (state, data) => {
        state.DrawFeatureData = data;
    },
    commitRasterData: (state, data) => {
        state.RasterData = data;
    },
    commitRasterLayerInfo: (state, data) => {
        state.RasterLayerInfo = data;
    },
};

export default {
    state,
    getters,
    actions,
    mutations,
};
