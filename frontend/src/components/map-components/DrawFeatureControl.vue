<template>
    <div
        class="block my-5 border-2 rounded"
        :class="collapse ? 'border-white' : 'border-gray-100'"
    >
        <div
            class="flex flex-row justify-between items-center cursor-pointer bg-gray-100 rounded px-3 py-3 transition-all duration-500"
            @click="collapse = !collapse"
        >
            <p>Draw feature control</p>
            <span
                :class="collapse ? 'rotate-0' : 'rotate-180'"
                class="fill-current h-6 w-6 transform transition-transform duration-500"
            >
                <unicon
                    :class="collapse ? 'animate-bounce' : ''"
                    name="angle-down"
                    fill="black"
                ></unicon>
            </span>
        </div>
        <div
            :class="collapse ? 'max-h-0' : 'max-h-96'"
            class="overflow-hidden transition-all duration-500 pl-5 pt-2 pr-2"
        >
            <label class="block mb-3">
                <span class="text-gray-700">Select the layer</span>
                <select
                    class="form-multiselect block w-full mt-1 rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
                    v-model="modelValue"
                >
                    <option
                        v-for="(option, index) in drawLayerOptions"
                        :key="index"
                        :value="option"
                        >{{ option }}</option
                    >
                </select>
            </label>
            <span class="text-gray-700">Layer: {{ modelValue }}</span>
            <div
                class="bg-gray-100 my-2 py-2 px-4 rounded-md max-h-72 overflow-auto"
            >
                <div v-if="!activeFeaturesDrawn.length">
                    No features drawn.
                </div>
                <div
                    v-for="(feature, index) in activeFeaturesDrawn"
                    :key="index"
                    class="my-2"
                >
                    <p class="text-lg my-1">
                        <span class="font-medium">{{ feature.type }}</span>
                        with id: {{ feature.id }}
                    </p>
                    <p
                        v-for="(latlng, index) in feature.latlngs"
                        :key="index"
                        class="text-sm"
                    >
                        {{ latlng }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { eventHub } from "src/event-hub";

export default {
    name: "DrawFeatureControl",
    data() {
        return {
            collapse: true,
        };
    },
    methods: {
        ...mapActions(["activateDrawFeatureLayer"]),
    },
    computed: {
        ...mapGetters(["getDrawFeatureData"]),
        drawLayerOptions() {
            var options = [];
            this.getDrawFeatureData.forEach((element) => {
                options.push(element.name);
            });
            return options;
        },
        activeFeaturesDrawn() {
            return this.getDrawFeatureData.find(
                (element) => element.active == true
            ).featuresDrawn;
        },
        modelValue: {
            get() {
                return this.getDrawFeatureData.find(
                    (element) => element.active == true
                ).name;
            },
            set(newValue) {
                this.activateDrawFeatureLayer(newValue);
                eventHub.$emit("changeDrawFeatureLayer");
            },
        },
    },
};
</script>

<style></style>
