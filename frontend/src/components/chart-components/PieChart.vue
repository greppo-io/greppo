<script>
import { Pie } from "vue-chartjs";

export default {
    extends: Pie,
    props: {
        data: String,
    },
    data: () => ({
        chartdata: {
            labels: ["VueJs", "EmberJs", "ReactJs", "AngularJs"],
            datasets: [
                {
                    backgroundColor: [
                        "#41B883",
                        "#E46651",
                        "#00D8FF",
                        "#DD1B16",
                    ],
                    data: [40, 20, 80, 10],
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
