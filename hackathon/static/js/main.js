$(document).ready(function(){
	var chart = new Highcharts.Chart({
		chart: {
			renderTo: 'myChart',
			type: 'area'
		},
		credits : {
			enabled : false
		},
		title: {
			text: 'Hermes'
		},
		xAxis: {
			categories: ["January","February","March","April","May","June","July","August","Septemper","October","November","December"]
		},
		yAxis: {
			title: {
				text: 'Total Trades'
			}
		},
		series: [{
			name: 'Web',
			data : [65,59,90,81,56,55,40,45,69,70,32,10]
		}, {
			name: 'Java',
			data: [28,48,40,19,96,27,100,43,78,88,45,50]
		}, {
			name: 'Database',
			data: [23,65,13,87,12,56,76,23,43,12,76,88]
		}]
	});
	// MASTER TROLE 2013
	setInterval(function() {
		var newData1 = [],
			newData2 = [],
			newData3 = [];
		for (var i = 0; i < 12; i++) {
			newData1[i] = Math.floor(Math.random()*100);
			newData2[i] = Math.floor(Math.random()*100);
			newData3[i] = Math.floor(Math.random()*100);
		}
		chart.series[0].setData(newData1);
		chart.series[1].setData(newData2);
		chart.series[2].setData(newData3);
	}, 1000);
});
