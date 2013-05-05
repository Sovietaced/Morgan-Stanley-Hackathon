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
			data : [0]
		}, {
			name: 'Java',
			data: [0]
		}, {
			name: 'Database',
			data: [0]
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
			categories: [],
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
			data : [0]
		}, {
			name: 'Europe',
			data : [0]
		}, {
			name: 'Asia',
			data : [0]
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
			data: []
		},{
			name: 'Profit',
			color: '#27AE60',
			data: []
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
			data: []
		},{
			name: 'Supply',
			data: []
		}]
	});

	// Allows for the dragging and dropping of dashboard components
	$("#sortable_container").sortable({
		update: function(event, ui) {
			$('[data-spy="scroll"]').each(function () {
				$(this).scrollspy('refresh');
			});
		}
	});

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
	var startGameButton = $('#start_game_button'),
		speedUpButton = $('#speed_up_button'),
		slowDownButton = $('#slow_down_button'),
		stopGameButton = $('#stop_game_button'),
		currentNum = 1;
		nextTurnButton = $('#next_turn_button');

	startGameButton.on('click', function(e) {
		var el = $(this);
		if (!el.hasClass('disabled')) {
			$.post('/game/start/', function(response) {
				$('#game_controls').find('.response').html(make_message(response.status, response.message));
				//if (response.status === 'success') {
					enableGameControls([speedUpButton, slowDownButton, stopGameButton]);
					disableGameControls([startGameButton]);
					//getNextTurn(1);
				//}
			},'json');
		}
	});

	nextTurnButton.on('click', function(e) {
		e.preventDefault();
		getTurn(currentNum);
	});

	speedUpButton.on('click', function(e) {
		var el = $(this);
	});

	slowDownButton.on('click', function(e) {
		var el = $(this);
	});

	stopGameButton.on('click', function(e) {
		var el = $(this);g
		disableGameControls([speedUpButton, slowDownButton, stopGameButton]);
		enableGameControls([startGameButton]);
	});

	var getTurn = function(num) {
		$.post('/turn/' + num, function(response) {
			if (response) {
				response = deserializeAgain(response);
				console.log(response);
				currentNum += 1;
				var profitSpan = $('.positive_profit');
				setTotalProfit(convertToDollars(response.profit[0].fields.total_profit));
				setConfigGraph(response.config);
				setDemandByRegionGraph(response.demands);
			}
		},'json');
	};

	var deserializeAgain = function(ar) {
		// Workaround method for having to serialize each element of array
		// in the Django controller
		var result = {};
		$.each(ar, function(idx, val) {
			result[idx] = JSON.parse(val);
		});
		return result;
	};

	var convertToDollars = function(cents) {
		return (parseFloat(cents)/100).toFixed(2);
	};

	var setTotalProfit = function(dollars) {
		var profit = $('.profit');
		if (dollars >= 0) {
			profit.removeClass('negative_profit').addClass('positive_profit');
		} else {
			profit.removeClass('positive_profit').addClass('negative_profit');
		}
		profit.html('$' + dollars);
	};

	var setConfigGraph = function(configArray) {
		var webTier = 0,
			javaTier = 0,
			dbTier = 0;
		$.each(configArray, function(idx, val) {
			if (val.fields.tier === 1) {
				webTier += parseInt(val.fields.count);
			} else if (val.fields.tier === 2) {
				javaTier += parseInt(val.fields.count);
			} else if (val.fields.tier === 3) {
				dbTier += parseInt(val.fields.count);
			}
		});
		totalCountsChart.series[0].setData([webTier]);
		totalCountsChart.series[1].setData([javaTier]);
		totalCountsChart.series[2].setData([dbTier]);
	};

	var setDemandByRegionGraph = function(demandArray) {
		var na = 0,
			eu = 0,
			ap = 0;
		$.each(demandArray, function(idx, val) {
			if (val.fields.region === 1) {
				na += parseInt(val.fields.count);
			} else if (val.fields.region === 2) {
				eu += parseInt(val.fields.count);
			} else if (val.fields.region === 3) {
				ap += parseInt(val.fields.count);
			}
		});
		demandByRegion.series[0].setData([na]);
		demandByRegion.series[1].setData([eu]);
		demandByRegion.series[2].setData([ap]);
	}

	var enableGameControls = function(btns) {
		$.each(btns, function(idx, val) {
			val.removeClass('disabled').tooltip('disable');
		});
	};

	var disableGameControls = function(btns) {
		$.each(btns, function(idx, val) {
			val.addClass('disabled').tooltip('enable');
		});
	};

	$('.twipsy').tooltip();

	var make_message = function (status, message) {
		if (status === 'success') {
			return '<div class="alert alert-success"><a class="close" data-dismiss="alert" href="#">&times;</a>' + message + '</div>';
		} else {
			return '<div class="alert alert-error"><a class="close" data-dismiss="alert" href="#">&times;</a>' + message + '</div>';
		}
	};
});
