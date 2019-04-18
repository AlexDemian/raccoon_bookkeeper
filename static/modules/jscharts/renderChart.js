function renderChart(chart_data, container_id) {
    
    var chart = new CanvasJS.Chart(container_id, {
        backgroundColor: "rgba(225,150,150,0)",
        height:350,
        width: 350,
        theme: "light2",
        exportFileName: "Name",
        exportEnabled: true,
        animationEnabled: false,
        title:{
            text: "Costs total"
        },
        legend:{
            cursor: "pointer",
            itemclick: explodePie
        },
        data: [{
            type: "doughnut",
            innerRadius: 50,
            showInLegend: false,
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
