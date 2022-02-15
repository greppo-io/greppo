<script>
import { Line } from "vue-chartjs";

export default {
    extends: Line,
    props: {
        chartData: Object,
    },
    data: () => ({
        chartOptions: {
            responsive: true,
            maintainAspectRatio: false,
        },
    }),
    mounted() {
        this.renderChart(this.chartData, this.chartOptions);
    },
};
</script>
