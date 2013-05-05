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
			text: 'Total Profit Potential'
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
			data: [0]
		},{
			name: 'Profit',
			color: '#27AE60',
			data: [0]
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
		nextTurnButton = $('#next_turn_button'),
		previousTurnButton = $('#previous_turn_button'),
		resumeGameButton = $('#resume_game_button'),
		clearErrorLogButton = $('#clear_error_log_button'),
		resetGameButton = $('#reset_game_button'),
		currentNum = 1,
		timeBetween = 1000,
		startGameRefresh = 0;

	startGameButton.on('click', function(e) {
		var el = $(this);
		if (!el.hasClass('disabled')) {
			$.post('/game/start/', function(response) {
				$('#game_controls').find('.response').html(make_message(response.status, response.message));
				if (response.status === 'success') {
					startGame();
				}
			},'json');
		}
	});

	nextTurnButton.on('click', function(e) {
		e.preventDefault();
		getTurn(currentNum);
	});

	previousTurnButton.on('click', function(e) {
		e.preventDefault();
		currentNum = currentNum - 2;
		getTurn(currentNum);
	});

	speedUpButton.on('click', function(e) {
		e.preventDefault();
		var el = $(this);
		timeBetween = timeBetween/2;
		setGameLoopTimer();
	});

	slowDownButton.on('click', function(e) {
		e.preventDefault();
		var el = $(this);
		timeBetween = timeBetween*2;
		setGameLoopTimer();
	});

	stopGameButton.on('click', function(e) {
		e.preventDefault();
		var el = $(this);
		stopGame();
	});

	resumeGameButton.on('click', function(e) {
		e.preventDefault();
		startGame();
	});

	resetGameButton.on('click', function(e) {
		e.preventDefault();
		currentNum = 1;
		timeBetween = 1000;
		setTotalProfit(0);
		setConfigGraph(0);
		setDemandByRegionGraph(0);
		setTotalProfitGraph(0);
		setTurnData(0);
		startGameButton.trigger('click');
	});

	clearErrorLogButton.on('click', function(e) {
		e.preventDefault();
		$('#error_log').find('tbody').children().empty();
	});

	var startGame = function() {
		enableGameControls([speedUpButton, slowDownButton, stopGameButton, nextTurnButton, previousTurnButton]);
		disableGameControls([startGameButton, resumeGameButton]);
		startGameRefresh = setInterval(getTurn, timeBetween);
	};

	var stopGame = function() {
		disableGameControls([speedUpButton, slowDownButton, stopGameButton]);
		enableGameControls([startGameButton, resumeGameButton]);
		clearInterval(startGameRefresh);
	};

	var setGameLoopTimer = function() {
		clearInterval(startGameRefresh);
		startGameRefresh = setInterval(getTurn, timeBetween);
	};

	var getTurn = function() {
		if (currentNum <= 0) {
			currentNum = 1;
		}
		$.post('/turn/' + currentNum, function(response) {
			if (response) {
				response = deserializeAgain(response);
				console.log(response);
				currentNum += 1;
				var profitSpan = $('.positive_profit');
				setTotalProfit(response.profit[0].fields.total_profit);
				setConfigGraph(response.config);
				setDemandByRegionGraph(response.demands);
				setTotalProfitGraph(response.profit[0].fields.total_potential);
				setTurnData(response.time);
			}
		},'json')
		.error(function() {
			var currentDate = new Date();
				addError("Could not retrieve turn " + currentNum + ". Have we reached the end of the game?", formatDate(currentDate));
		});
	};

	var formatDate = function(currentDate) {
		return currentDate.getDate() + "/"
			+ (currentDate.getMonth()+1)  + "/"
			+ currentDate.getFullYear() + " @ "
			+ currentDate.getHours() + ":"
			+ currentDate.getMinutes() + ":"
			+ currentDate.getSeconds();
	}

	var setTurnData = function(currentDate) {
		$('.turn_num').html(currentNum);
		$('.turn_date_time').html(currentDate);
	};

	var addError = function(message, timestamp) {
		var tbody = $('#error_log').find('tbody');
		tbody.append('<tr><td>' + message + '</td><td>' + timestamp + '</td></tr>');
	};

	var deserializeAgain = function(ar) {
		// Workaround method for having to serialize each element of array
		// in the Django controller
		var result = {};
		$.each(ar, function(idx, val) {
			if (idx !== 'time') {
				result[idx] = JSON.parse(val);
			} else {
				result[idx] = val;
			}
		});
		return result;
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
	};

	var setTotalProfitGraph = function(percent) {
		if (percent < 0) {
			percent = 0;
		}
		var loss = 100 - percent;
		totalProfit.series[0].setData([loss]);
		totalProfit.series[1].setData([percent]);
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
