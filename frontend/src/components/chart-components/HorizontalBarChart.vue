<script>
import { HorizontalBar } from "vue-chartjs";

export default {
    extends: HorizontalBar,
    props: {
        chartData: Object,
    },
    data: () => ({
        chartdata: {
            labels: [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            datasets: [
                {
                    label: "Data One",
                    backgroundColor: "#f87979",
                    data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11],
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        },
    }),

    mounted() {
        this.renderChart(this.chartdata, this.options);
    },
};
</script>
