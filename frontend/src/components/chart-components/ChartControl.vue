<template>
    <div class="my-10 mx-2">
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
