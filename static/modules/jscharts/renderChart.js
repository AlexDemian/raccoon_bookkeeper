
function renderChart(chart_data, container_id) {
    if (!chart_data.length) {
        return
    }
    var chart = new CanvasJS.Chart(container_id, {
        backgroundColor: "rgba(225,150,150,0)",
        height: 350,
        width: 350,
        theme: "light2",
        exportFileName: "raccoonBookerChart",
        exportEnabled: true,
        animationEnabled: false,
        title:{
            text: "",
        },
        legend:{
            verticalAlign: "top",
            horizontalAlign: "left",
            cursor: "pointer",
            itemclick: explodePie,
            fontSize: 12,
            fontWeight: 'bold',
            fontColor:  'black'


        },

        toolTip:{
            enabled: true,
            animationEnabled: true,
            fontSize: 14,
            fontWeight: 'bold',
            fontColor:  'black'

        },

        data: [{
            type: "doughnut",
            innerRadius: 50,
            showInLegend: true,
            toolTipContent: "<b>{name}</b>: {y} (#percent%)",
            indexLabel: "{name} - #percent%",
            dataPoints: chart_data
        }]
    });
    chart.render();

    function explodePie (e) {
        if(typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
            e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
        } else {
            e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
        }
        e.chart.render();
    }

}
