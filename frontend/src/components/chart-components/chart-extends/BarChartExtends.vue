<script>
import { Bar } from "vue-chartjs";
import { pSBC } from "../../utils/color-space";

export default {
    extends: Bar,
    props: {
        chartData: Object,
        baseColor: Array,
        highlightStatus: Boolean,
    },
    data: () => ({
        chartOptions: {
            responsive: true,
            maintainAspectRatio: false,
            onClick: null,
        },
    }),
    watch: {
        highlightStatus: function() {
            if (!this.highlightStatus) {
                this.unhighlightBar();
            }
        },
    },
    methods: {
        handleChartClick(event, elements) {
            if (elements.length !== 0) {
                const chart = this.$data._chart;
                const chartEvent = chart.getElementAtEvent(event)[0];

                const _datasetIndex = chartEvent._datasetIndex;
                const _datasetLabel = chartEvent._model.datasetLabel;
                const _dataIndex = chartEvent._index;
                const _dataLabel = chartEvent._model.label;
                const _dataValue =
                    chartEvent._chart.data.datasets[_datasetIndex].data[
                        _dataIndex
                    ];

                const clickData = {
                    datasetIndex: _datasetIndex,
                    datasetLabel: _datasetLabel,
                    dataIndex: _dataIndex,
                    dataLabel: _dataLabel,
                    dataValue: _dataValue,
                };
                
                this.highlightBar(_datasetIndex, _dataIndex);
                this.$emit("highlightEvent", {"status": true, "clickData": clickData});
            }
        },
        highlightBar(_datasetIndex, _dataIndex) {
            // Method to highlight the selected element on the chart.
            this.$data._chart.data.datasets.forEach((dataset, indexI) => {
                for (
                    var indexJ = 0;
                    indexJ < dataset.backgroundColor.length;
                    indexJ++
                ) {
                    if (indexI === _datasetIndex && indexJ === _dataIndex) {
                        // dataset.backgroundColor[indexJ] = "#f31616";
                        dataset.backgroundColor[indexJ] = pSBC(
                            -0.1,
                            this.baseColor[_datasetIndex]
                        );
                    } else {
                        // dataset.backgroundColor[indexJ] = "#faa8a8";
                        dataset.backgroundColor[indexJ] = pSBC(
                            0.7,
                            this.baseColor[_datasetIndex]
                        );
                    }
                }
            });
            this.$data._chart.update();
        },
        unhighlightBar() {
            // Method to un-highlight the selected element on the chart.
            this.$data._chart.data.datasets.forEach((dataset, indexI) => {
                for (
                    var indexJ = 0;
                    indexJ < dataset.backgroundColor.length;
                    indexJ++
                ) {
                    dataset.backgroundColor[indexJ] = this.baseColor[indexI];
                }
            });
            this.$data._chart.update();
            this.highlight = false;
        },
    },
    created() {
        // Adds the click handler for the chart.
        this.chartOptions.onClick = this.handleChartClick;
    },
    mounted() {
        this.renderChart(this.chartData, this.chartOptions);
    },
};
</script>
