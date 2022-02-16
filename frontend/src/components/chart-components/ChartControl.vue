<template>
    <div class="my-10 mx-2" v-if="data.type === 'BarChart' || data.type === 'LineChart'" >
        <p class="text-xl my-1">{{ data.name }}</p>
        <p class="text-base my-1">{{ data.description }}</p>
        <bar-chart
            v-if="data.type == 'BarChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <line-chart
            v-if="data.type == 'LineChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <bubble-chart
            v-if="data.type == 'BubbleChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <doughnut-chart
            v-if="data.type == 'DoughnutChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <horizontal-bar-chart
            v-if="data.type == 'HorizontalBarChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <pie-chart
            v-if="data.type == 'PieChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <polar-chart
            v-if="data.type == 'PolarChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <radar-chart
            v-if="data.type == 'RadarChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
        <scatter-chart
            v-if="data.type == 'ScatterChart'"
            :id="data.id"
            :chartData="data.chartdata"
            style="height: 250px"
        />
    </div>
</template>

<script>
import BarChart from "./BarChart";
import BubbleChart from "./BubbleChart.vue";
import DoughnutChart from "./DoughnutChart.vue";
import HorizontalBarChart from "./HorizontalBarChart.vue";
import LineChart from "./LineChart";
import PieChart from "./PieChart.vue";
import PolarChart from "./PolarChart.vue";
import RadarChart from "./RadarChart.vue";
import ScatterChart from "./ScatterChart.vue";

export default {
    name: "ChartControl",
    props: {
        data: Object,
    },
    components: {
        BarChart,
        BubbleChart,
        DoughnutChart,
        HorizontalBarChart,
        LineChart,
        PieChart,
        PolarChart,
        RadarChart,
        ScatterChart,
    },
    data() {
        return {
            // Delete after implementing charts.
            chartTetst: {
                labels: ["January", "February", "March", "April"],
                datasets: [
                    {
                        label: "Data One",
                        backgroundColor: "#f87979",
                        data: [40, 20, 30, 50],
                    },
                    {
                        label: "Data Two",
                        backgroundColor: "#f87979",
                        data: [20, 10, 60, 40],
                    },
                ],
            },
        };
    },
};
</script>

<style></style>
