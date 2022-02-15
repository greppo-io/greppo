<script>
import { Bar } from "vue-chartjs";

export default {
    extends: Bar,
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
