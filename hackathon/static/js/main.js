$(document).ready(function(){
	var totalCountsChart = new Highcharts.Chart({
		chart: {
			renderTo: 'total_counts',
			type: 'column'
		},
		credits : {
			enabled : false
		},
		title: {
			text: 'Current Total Configuration Counts'
		},
		xAxis: {
			categories: ['Current']
		},
		yAxis: {
			title: {
				text: 'Count'
			}
		},
		series: [{
			name: 'Web',
			data : [4]
		}, {
			name: 'Java',
			data: [3]
		}, {
			name: 'Database',
			data: [2]
		}]
	});

	var demandByRegion = new Highcharts.Chart({
		chart: {
			renderTo: 'demand_by_region',
			type: 'line'
		},
		credits : {
			enabled : false
		},
		title: {
			text: 'Current Demand By Region'
		},
		xAxis: {
			categories: ['12:00:00','12:00:30','12:01:00','12:01:30'],
			title: {
				text: 'Time'
			}
		},
		yAxis: {
			title: {
				text: 'Transaction Count'
			}
		},
		series: [{
			name: 'North America',
			data : [200,240,450,349]
		}, {
			name: 'Europe',
			data : [4,60,200,250]
		}, {
			name: 'Asia',
			data : [400,410,420,430]
		}]
	});

	var totalProfit = new Highcharts.Chart({
		chart: {
			renderTo: 'total_profit',
			type: 'column'
		},
		credits : {
			enabled : false
		},
		title: {
			text: 'Total Profit'
		},
		xAxis: {
			categories: ['Profit','Loss'],
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Percentage of Total Profit'
			}
		},
		plotOptions: {
			column: {
				stacking: 'percent'
			}
		},
		series: [{
			name: 'Loss',
			color: '#E74C3C',
			data: [20]
		},{
			name: 'Profit',
			color: '#27AE60',
			data: [80]
		}]
	});

	var demandVsSupply = new Highcharts.Chart({
		chart: {
			renderTo: 'demand_vs_supply',
			type: 'column'
		},
		credits : {
			enabled : false
		},
		title: {
			text: 'Demand vs. Supply'
		},
		xAxis: {
			categories: ['NA Web','NA Java','NA DB','EU Web','EU Java','EU DB','AP Web','AP Java','AP DB'],
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Transactions'
			}
		},
		series: [{
			name: 'Demand',
			data: [95,300,650,175,376,987,43,80,100]
		},{
			name: 'Supply',
			data: [180,400,1000,180,400,1000,180,400,1000]
		}]
	});

	// Allows for the dragging and dropping of dashboard components
	//$("#sortable_container").sortable();

	// Make the links pretty when you click them
	var nav_links = $('.nav').find('li');
	$('.nav').on('click', 'a', function(e) {
		var el = $(this),
			parent = el.parent();
		$.each(nav_links, function(idx, val) {
			$(val).removeClass('active');
		});
		parent.addClass('active');
	});

	// Account for the sticky navbar
	$('.navbar li a').click(function(event) {
		event.preventDefault();
		$($(this).attr('href'))[0].scrollIntoView();
		scrollBy(0, -45);
	});

	$('.tablesorter').tablesorter();
	//$('body').scrollspy({offset:'45'});
});
