import axios from "axios";
import { eventHub } from "src/event-hub";

// const average = (array) => array.reduce((a, b) => a + b) / array.length;

// Status codes
// 1: Created application
// 2: Fetch data finished
// 3: Draw visualization

const state = {
    Status: 1,
    ComponentStatus: {
        baseLayer: false,
        tileLayer: false,
        wmstileLayer: false,
        vectorLayer: false,
        overlayLayer: false,
        imageLayer: false,
        mapComponent: false,
        inputComponent: false,
        drawFeature: false,
    },
    AppInfo: {
        modal: false,
        title: null,
        description: null,
    },
    ErrorModal: {
        status: false,
        message: "",
    },
    VectorLayerData: null,
    ImageLayerData: null,
    BaseLayerData: null,
    TileLayerData: null,
    WMSTileLayerData: null,
    OverlayLayerInfo: null,
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
};

const getters = {
    getStatus: (state) => state.Status,
    getAppInfo: (state) => state.AppInfo,
    getInfoModal: (state) => state.InfoModal,
    getErrorModal: (state) => state.ErrorModal,
    getComponentStatus: (state) => state.ComponentStatus,
    getVectorLayerData: (state) => state.VectorLayerData,
    getBaseLayerData: (state) => state.BaseLayerData,
    getTileLayerData: (state) => state.TileLayerData,
    getWMSTileLayerData: (state) => state.WMSTileLayerData,
    getOverlayLayerInfo: (state) => state.OverlayLayerInfo,
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
    getImageLayerData: (state) => state.ImageLayerData,
};

const actions = {
    setAppInfo({ commit, state }, dataAppInfo) {
        var AppInfo = state.AppInfo;
        if ("modal" in dataAppInfo) {
            AppInfo.modal = dataAppInfo.modal;
        }
        if ("title" in dataAppInfo) {
            AppInfo.title = dataAppInfo.title;
        }
        if ("description" in dataAppInfo) {
            AppInfo.description = dataAppInfo.description;
        }
        commit("commitAppInfo", AppInfo);
    },

    setErrorModal({ commit, state }, dataErrorModal) {
        var ErrorModal = state.ErrorModal;
        if ("status" in dataErrorModal) {
            ErrorModal.status = dataErrorModal.status;
        }
        if ("message" in dataErrorModal) {
            ErrorModal.message = dataErrorModal.message;
        }
        commit("commitErrorModal", ErrorModal);
    },

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
                postData[drawFeature.name] =
                    drawFeature.featuresDrawn.map(mapDrawFeature);
            }
        });

        axios
            .post(process.env.VUE_APP_API, postData)
            .then(function (response) {
                dispatch("commitResponseData", response);
                commit("commitInputMutation", false);
                eventHub.$emit("reInitializeDrawFeature");
            })
            .catch(function (error) {
                // TODO Frontend error logging
                console.log("Error in posting data.", error);
            });
    },

    commitResponseData({ commit, state, dispatch }, response) {
        var ComponentStatus = state.ComponentStatus;

        console.log(response.data);
        const responseBaseLayerData = response.data.base_layer_data;
        const responseTileLayerData = response.data.tile_layer_data;
        const responseWMSTileLayerData = response.data.wms_tile_layer_data;
        const responseVectorLayerData = response.data.vector_layer_data;
        const responseImageLayerData = response.data.image_layer_data;
        const responseComponentInfo = response.data.component_info;

        var overlayLayerInfo = [];

        if (responseBaseLayerData.length) {
            ComponentStatus.baseLayer = true;
            commit("commitBaseLayerData", responseBaseLayerData);
        }

        if (responseTileLayerData.length) {
            ComponentStatus.tileLayer = true;
            ComponentStatus.overlayLayer = true;
            commit("commitTileLayerData", responseTileLayerData);

            responseTileLayerData.forEach(function (layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    name: layerData.name,
                    description: layerData.description,
                    visible: layerData.visible,
                    bounds: [],
                    color: "#10B981",
                });
            });
        }

        if (responseWMSTileLayerData.length) {
            ComponentStatus.wmstileLayer = true;
            ComponentStatus.overlayLayer = true;
            commit("commitWMSTileLayerData", responseWMSTileLayerData);

            responseWMSTileLayerData.forEach(function (layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    name: layerData.name,
                    description: layerData.description,
                    visible: layerData.visible,
                    bounds: [],
                    color: "#10B981",
                });
            });
        }

        if (responseImageLayerData.length) {
            ComponentStatus.imageLayer = true;
            ComponentStatus.overlayLayer = true;
            commit("commitImageLayerData", responseImageLayerData);

            responseImageLayerData.forEach(function (layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    name: layerData.name,
                    description: layerData.description,
                    visible: layerData.visible,
                    bounds: layerData.bounds,
                    color: "#10B981",
                });
            });
        }

        if (responseVectorLayerData.length) {
            ComponentStatus.vectorLayer = true;
            ComponentStatus.overlayLayer = true;
            commit("commitVectorLayerData", responseVectorLayerData);

            responseVectorLayerData.forEach(function (layerData) {
                overlayLayerInfo.push({
                    id: layerData.id,
                    name: layerData.name,
                    description: layerData.description,
                    visible: layerData.visible,
                    bounds: layerData.bounds,
                    color: "#10B981",
                });
            });
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
                if (component.type === "Display") {
                    if (component.name === "title") {
                        dispatch("setAppInfo", { title: component.value });
                    }
                    if (component.name === "description") {
                        dispatch("setAppInfo", {
                            description: component.value,
                        });
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
    commitAppInfo: (state, data) => {
        state.AppInfo = data;
    },
    commitErrorModal: (state, data) => {
        state.ErrorModal = data;
    },
    commitVectorLayerData: (state, data) => {
        state.VectorLayerData = data;
    },
    commitBaseLayerData: (state, data) => {
        state.BaseLayerData = data;
    },
    commitTileLayerData: (state, data) => {
        state.TileLayerData = data;
    },
    commitWMSTileLayerData: (state, data) => {
        state.WMSTileLayerData = data;
    },
    commitOverlayLayerInfo: (state, data) => {
        state.OverlayLayerInfo = data;
    },
    commitInputMutation: (state, data) => {
        state.InputMutation = data;
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
        state.BaseLayerData.forEach((layer) => {
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
    commitImageLayerData: (state, data) => {
        state.ImageLayerData = data;
    },
};

export default {
    state,
    getters,
    actions,
    mutations,
};
