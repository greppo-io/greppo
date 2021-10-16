<template>
    <div>
        <!-- This will run a v-for with ids across all the requested charts to be displayed. -->
        <bar-chart style="height: 250px;" :chartData="chartDataBar1" />
        <bar-chart style="height: 250px;" :chartData="chartDataBar2" />
        <div v-if="false">
            <line-chart style="height: 250px;" data="Line" />
            <pie-chart style="height: 250px;" data="Pie" />
            <doughnut-chart style="height: 250px;" data="Doughnut" />
            <radar-chart style="height: 250px;" data="Radar" />
            <polar-chart style="height: 250px;" data="Polar" />
            <bubble-chart style="height: 250px;" data="Bubble" />
            <scatter-chart style="height: 250px;" data="Scatter" />
            <horizontal-bar-chart style="height: 250px;" data="Horizontal Bar"
            />
        </div>
    </div>
</template>

<script>
import BarChart from "./BarChart";
import LineChart from "./LineChart";
import PieChart from "./PieChart";
import DoughnutChart from "./DoughnutChart";
import RadarChart from "./RadarChart";
import PolarChart from "./PolarChart";
import BubbleChart from "./BubbleChart";
import ScatterChart from "./ScatterChart";
import HorizontalBarChart from "./HorizontalBarChart";

export default {
    name: "ChartContainer",
    components: {
        BarChart,
        LineChart,
        PieChart,
        DoughnutChart,
        RadarChart,
        PolarChart,
        BubbleChart,
        ScatterChart,
        HorizontalBarChart,
    },
    data() {
        return {
            chartDataBar1: {
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
            chartDataBar2: {
                labels: ["May", "June", "July", "August"],
                datasets: [
                    {
                        label: "Data Three",
                        backgroundColor: "#f87979",
                        data: [60, 80, 50, 20],
                    },
                    {
                        label: "Data Four",
                        backgroundColor: "#f87979",
                        data: [10, 50, 30, 80],
                    },
                ],
            },
        };
    },
};
</script>

<style></style>
