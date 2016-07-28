$(document).ready(function() { 
	var ws = new WebSocket("ws://localhost:80/websocket");

	ws.onopen = function() {
	   // ws.send("req");
	};

	ws.onmessage = function (evt) {
		payload = evt.data.split("&");
		var target = document.getElementById("snapshot");
		console.log('snapshot');
		console.log(evt.data);
		switch(payload[0]){
			case "state":
				target = document.getElementById("state");
				target.innerHTML = payload[1];
				// $("#loader").hide();
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
				target.innerHTML = "Average Time: " + payload[1];

				break;
			case "remaining":
				target = document.getElementById("remaining");
				target.innerHTML = "Estimated Remaining Time: " + payload[1] + "s";

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

				break;
			default:
				break;

		}
		// target.innerHTML = evt.data; // clear existing
		
		// var div = document.createElement('div');
		// var elements = div.childNodes;
		// span.appendChild(text);
	};
});
