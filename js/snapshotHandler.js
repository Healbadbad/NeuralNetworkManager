
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
