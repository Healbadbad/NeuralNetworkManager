var dataSetData = [];
var labels = [];

var ws = new WebSocket("ws://localhost:80/websocket");

ws.onopen = function() {
   // ws.send("req");
};

ws.onmessage = function (evt) {
	payload = evt.data.split("&");
	console.log(payload);
	if (payload[1] == 'Model Compiled.') {
		$("#loader").hide();
	}

	var target = document.getElementById("snapshot");
	switch(payload[0]){
		case "state":
			target = document.getElementById("state");
			target.innerHTML = payload[1];
			break;
		case "epoch":
			target = document.getElementById("epoch");
			target.innerHTML = "Epoch: " + payload[1];

			break;
		case "epochTarget":
			target = document.getElementById("epochTarget");
			target.innerHTML = "Target Epochs: " + payload[1];

			break;
		case "avgtime":
			target = document.getElementById("avgtime");
			target.innerHTML = "Average Time: " + formatTime(payload[1]);

			break;
		case "remaining":
			target = document.getElementById("remaining");
			target.innerHTML = "Estimated Remaining Time: " + formatTime(payload[1]);

			break;
		case "trainerr":
			target = document.getElementById("trainerr");
			target.innerHTML = "Training Error: " + payload[1];

			break;
		case "accuracy":
			target = document.getElementById("accuracy");
			target.innerHTML = "Accuracy: " + payload[1];

			break;
		case "snapshot":
			target = document.getElementById("snapshot");
			target.innerHTML = payload[1];
			plotChart();

			break;
		default:
			break;

	}
	// target.innerHTML = evt.data; // clear existing
	
	// var div = document.createElement('div');
	// var elements = div.childNodes;
	// span.appendChild(text);
};

var formatTime = function(t){
	total = parseFloat(t);
	if(total > 3600) {
		hours = Math.floor(total/3600);
		minutes = Math.floor((total%3600)/60);
		seconds = Math.floor((total%3600)%60);
		return hours + "h:" + minutes + "m:" + seconds + "s";
	} else if(total > 90){
		minutes = Math.floor(total/60);
		seconds = Math.floor(total%60);
		return minutes + "m:" + seconds + "s";
	} else {
		return t + "s";
	}

}

function plotChart() {
	var ws = new WebSocket("ws://localhost:80/accuracyLoss");

	ws.onopen = function() {
		console.log("accuracyloss listener connected!");
	};

	ws.onmessage = function (evt) {
		var dataSetData = [];
		var labels = [];
		var accAndErr = evt.data.split('\n');
		var accuracies = accAndErr[0].substring(1, accAndErr[0].length-1).split(",").map(Number);
		var trainErr =  accAndErr[1].substring(1, accAndErr[1].length-1).split(",").map(Number);
		console.log('accuracies and stuff');
		console.log(accuracies);
		console.log(trainErr);

		for (var i = 0; i < trainErr.length; i++) {
			dataSetData.push(accuracies[i] / trainErr[i]);
			labels[i] = "epoch" + (i+1);
		}
		console.log(dataSetData);

		var ctx = document.getElementById("myChart");
		var data = {
		    labels: labels,
		    datasets: [
		        {
		            label: "Accuracy / Loss",
		            fill: false,
		            lineTension: 0.1,
		            backgroundColor: "rgba(75,192,192,0.4)",
		            borderColor: "rgba(75,192,192,1)",
		            borderCapStyle: 'butt',
		            borderDash: [],
		            borderDashOffset: 0.0,
		            borderJoinStyle: 'miter',
		            pointBorderColor: "rgba(75,192,192,1)",
		            pointBackgroundColor: "#fff",
		            pointBorderWidth: 1,
		            pointHoverRadius: 5,
		            pointHoverBackgroundColor: "rgba(75,192,192,1)",
		            pointHoverBorderColor: "rgba(220,220,220,1)",
		            pointHoverBorderWidth: 2,
		            pointRadius: 1,
		            pointHitRadius: 10,
		            data: dataSetData,
		            spanGaps: false,
		        }
		    ],
		    xAxisID: "Training Error",
		    yAxisID: "Accuracy"

		};

		var options = {
			responsive: true,
	        title: {
	            display: true,
	            text: 'Accuracy / Loss in Neural Network'
	        },
	        legend: {
	        	display: false,
	        	position: "top",
	        	labels: {
	                fontColor: 'rgb(255, 99, 132)'
	            }
	        },
	        scales: {
	        	xAxes: [{
	        		display: true
	        	}],
	            yAxes: [{
	                display: true,
	                scaleLabel: {
				        display: true,
				        labelString: 'Accuracy/Loss'
				    }
	            }]
	        },
	        scaleShowLabels : true
	    };

		var myLineChart = new Chart(ctx, {
		    type: 'line',
		    data: data,
		    options: options
		});
		ctx.style.width = "95%";
	};

}