<template>
    <div class="relative p-3 pt-16 bg-white h-full overflow-auto">
        <!-- Implement the switch case for the type of input component.type -->
        <button
            class="absolute hover:bg-red-500 focus:outline-none bg-red-600 rounded text-white px-8 py-2 text-sm right-7 top-7"
            v-if="getInputMutation"
            @click="postAPI"
        >
            Update
        </button>

        <button
            class="absolute focus:outline-none bg-gray-300 rounded text-white px-8 py-2 text-sm right-7 top-7"
            v-if="!getInputMutation"
            disabled            
        >
            Update
        </button>

        <layer-control v-show="true" />

        <draw-feature-control v-if="getComponentStatus.drawFeature" />

        <div v-for="component in getInputComponentInfo" :key="component.id">
            <input-control :data="component" />
            <chart-control :data="component" />
        </div>
        
    </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import LayerControl from "./map-components/LayerControl";
import InputControl from "./input-components/InputControl.vue";
import ChartControl from "./chart-components/ChartControl.vue";
import DrawFeatureControl from "./map-components/DrawFeatureControl.vue";

export default {
    name: "LeftContainer",
    components: {
        LayerControl,
        InputControl,
        ChartControl,
        DrawFeatureControl,
    },
    methods: mapActions(["postAPI"]),
    computed: mapGetters([
        "getInputComponentInfo",
        "getInputMutation",
        "getComponentStatus",
    ]),
};
</script>

<style></style>
