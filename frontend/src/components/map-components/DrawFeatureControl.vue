<template>
    <div class="block my-5">
        <div
            :class="collapse ? 'bg-gray-100' : 'bg-white'"
            class="flex flex-row justify-between items-center cursor-pointer rounded px-3 py-3 transition-all duration-500"
            @click="collapse = !collapse"
        >
            <p>Draw feature control</p>
            <span
                :class="collapse ? 'rotate-0' : 'rotate-180'"
                class="fill-current h-6 w-6 transform transition-transform duration-500"
            >
                <unicon name="angle-down" fill="black"></unicon>
            </span>
        </div>
        <div
            :class="collapse ? 'max-h-0' : 'max-h-96'"
            class="overflow-hidden transition-all duration-500 pl-5 pt-2"
        >
            <span class="text-gray-700">{{ getDefaultDrawFeatures.name }}</span>
            <div
                class="bg-gray-100 my-2 py-2 px-4 rounded-md max-h-72 overflow-auto"
            >
                <div v-if="!getDrawnFeatures.length">
                    No features drawn.
                </div>
                <div
                    v-for="(feature, index) in getDrawnFeatures"
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
import { mapGetters } from "vuex";
export default {
    name: "DrawFeatureControl",
    data() {
        return {
            collapse: true,
        };
    },
    computed: mapGetters(["getDrawnFeatures", "getDefaultDrawFeatures"]),
};
</script>

<style></style>
