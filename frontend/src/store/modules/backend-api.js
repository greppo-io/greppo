import axios from "axios";

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
    DrawFeatureState: false,
    // Draw features that are passsed from the backend.
    DefaultDrawFeatures: {
        name: "Default features",
        features: [],
        mutation: false,
    },
    DrawnFeatures: [],
    InputMutation: false,
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
    getDrawFeatureState: (state) => state.DrawFeatureState,
    getDefaultDrawFeatures: (state) => state.DefaultDrawFeatures,
    getDrawnFeatures: (state) => state.DrawnFeatures,
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

        if (state.DefaultDrawFeatures.mutation) {
            postData[state.DefaultDrawFeatures.name] = state.DrawnFeatures;
        }

        axios
            .post(process.env.VUE_APP_API, postData)
            .then(function(response) {
                dispatch("commitResponseData", response);
                commit("commitInputMutation", false);
                commit("commitDrawFeatureMutation", false);
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

        if (responseBaseLayerInfo.length) {
            ComponentStatus.baseLayer = true;
            commit("commitBaseLayerInfo", responseBaseLayerInfo);
        }

        if (responseVectorData.length) {
            ComponentStatus.overlayLayer = true;
            commit("commitVectorData", responseVectorData);

            let overlayLayerInfo = [];
            let viewzoomInfo = [];
            responseVectorData.forEach(function(layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    title: layerData.title,
                    description: layerData.description,
                    visible: layerData.visible,
                    color: layerData.style.fillColor,
                });
                viewzoomInfo.push({
                    id: layerData.id,
                    viewzoom: layerData.viewzoom,
                });
            });
            commit("commitOverlayLayerInfo", overlayLayerInfo);

            // Commit zoom and view, 1st step just average the x,y and min of zoom.
            // Next based on the visible layers.
            const viewzoom = [
                average(viewzoomInfo.map((a) => a.viewzoom[0])),
                average(viewzoomInfo.map((a) => a.viewzoom[1])),
                Math.min(...viewzoomInfo.map((a) => a.viewzoom[2])),
            ];
            commit("commitViewZoom", viewzoom);
        }

        if (responseComponentInfo.length) {
            ComponentStatus.inputComponent = true;

            commit("commitInputComponentInfo", responseComponentInfo);            

            const index_draw = responseComponentInfo.findIndex(
                (component) => component.type === "DrawFeature"
            );
            if (index_draw !== -1) {
                ComponentStatus.drawFeature = true;
                commit("commitDrawFeatureState", true);
                commit("commitDefaultDrawFeatures", {
                    name: responseComponentInfo[index_draw].name,
                    features: responseComponentInfo[index_draw].features,
                    mutation: false,
                });
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

    addDrawnFeature({ commit, state }, newFeature) {
        const featuresState = state.DrawnFeatures;
        featuresState.push(newFeature);
        commit("commitDrawnFeatures", featuresState);
    },

    editDrawnFeatures({ commit, state }, editFeatures) {
        const featuresState = state.DrawnFeatures;
        editFeatures.forEach((editElement) => {
            const index = featuresState.findIndex(
                (feature) => feature.id === editElement.id
            );
            if (index !== -1) {
                featuresState[index].latlngs = editElement.latlngs;
            }
        });
        commit("commitDrawnFeatures", featuresState);
    },

    deleteDrawnFeatures({ commit, state }, deleteFeatures) {
        const featuresState = state.DrawnFeatures;
        deleteFeatures.forEach((editElement) => {
            const index = featuresState.findIndex(
                (feature) => feature.id === editElement.id
            );
            if (index !== -1) {
                featuresState.splice(index, 1);
            }
        });
        commit("commitDrawnFeatures", featuresState);
    },

    setDrawFeatureMutation({ commit, state }, mutationState) {
        commit("commitDrawFeatureMutation", mutationState);
        if (!state.InputMutation) {
            commit("commitInputMutation", true);
        }
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
    commitDrawFeatureState: (state, data) => {
        state.DrawFeatureState = data;
    },
    commitDefaultDrawFeatures: (state, data) => {
        state.DefaultDrawFeatures = data;
    },
    commitDrawFeatureMutation: (state, data) => {
        state.DefaultDrawFeatures.mutation = data;
    },
    commitDrawnFeatures: (state, data) => {
        state.DrawnFeatures = data;
    },
};

export default {
    state,
    getters,
    actions,
    mutations,
};
