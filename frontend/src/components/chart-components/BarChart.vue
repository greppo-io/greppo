<template>
    <div class="my-10">
        <p class="text-xl">{{ title }}</p>
        <p class="text-base">{{ description }}</p>
        <p class="text-sm" v-if="highlightStatus">
            Selected: {{ selectedData.dataLabel }},
            {{ selectedData.dataValue }} of {{ selectedData.datasetLabel }}
            <button
                class="mx-2 my-2 bg-white transition duration-150 ease-in-out hover:bg-gray-100 rounded text-indigo-700 px-3 py-1 text-sm focus:outline-none"
                @click="resetClick"
            >
                Reset
            </button>
        </p>
        <bar-chart-extends
            style="height: 250px;"
            :chartData="chartData"
            :baseColor="baseColor"
            :highlightStatus="highlightStatus"
            @highlightEvent="handleHighlightEvent"
        />
    </div>
</template>

<script>
import BarChartExtends from "./chart-extends/BarChartExtends.vue";
import { mapActions } from "vuex";

export default {
    name: "BarChart",
    props: {
        id: String,
        title: String,
        description: String,
        chartData: Object,
    },
    components: {
        BarChartExtends,
    },
    data() {
        return {
            baseColor: [],
            highlightStatus: false,
            selectedData: {},
        };
    },
    methods: {
        ...mapActions(["setChartEventData"]),
        resetClick() {
            this.highlightStatus = false;
            this.selectedData = {};
        },
        handleHighlightEvent(eventData) {
            this.highlightStatus = eventData.status;
            this.selectedData = eventData.clickData;
            this.setChartEventData(eventData.clickData);
        },
    },
    created() {
        // Creates an array of the background color data variable in the dataset
        // object using the color input from the prop.
        this.baseColor = new Array(this.chartData.datasets.length).fill(
            "#CCCCCC"
        );
        this.chartData.datasets.forEach((dataset, index) => {
            if (dataset.data.length > 1) {
                if (dataset.backgroundColor.constructor !== Array) {
                    this.baseColor[index] = dataset.backgroundColor;
                    dataset.backgroundColor = new Array(
                        dataset.data.length
                    ).fill(dataset.backgroundColor);
                } else if (
                    dataset.backgroundColor.length !== dataset.data.length
                ) {
                    this.baseColor[index] = dataset.backgroundColor[0];
                    dataset.backgroundColor = new Array(
                        dataset.data.length
                    ).fill(dataset.backgroundColor[0]);
                }
            } else {
                if (dataset.backgroundColor.constructor === Array) {
                    this.baseColor[index] = dataset.backgroundColor[0];
                } else {
                    this.baseColor[index] = dataset.backgroundColor;
                }
            }
        });
    },
};
</script>

<style></style>
