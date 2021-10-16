<template>
    <div>
        <bar-chart
            v-if="data.type == 'BarChart'"
            :id="data.id"
            :title="data.title"
            :description="data.description"
            :chartData="data.chartdata"
        />
        <line-chart
            v-if="data.type == 'LineChart'"
            :id="data.id"
            :title="data.title"
            :description="data.description"
            :chartData="data.chartdata"
        />
    </div>
</template>

<script>
import BarChart from "./BarChart";
import LineChart from "./LineChart";

export default {
    name: "ChartControl",
    props: {
        data: Object,
    },
    components: {
        BarChart,
        LineChart,
    },
    data() {
        return {
            // Delete after implementing charts.
            chartTetst1: {
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
            chartTetst2: {
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
