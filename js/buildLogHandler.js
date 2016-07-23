var ws = new WebSocket("ws://localhost:80/buildSocket");

ws.onopen = function() {
	console.log("Build Log connected!");
};

ws.onmessage = function (evt) {
	// console.log("received message: " + evt.data);
	var target = document.getElementById("logFeed");
	var div = document.createElement('div');
	target.innerHTML = target.innerHTML + evt.data; // clear existing
	var elements = div.childNodes;
	target.scrollTop = target.scrollHeight;
	// span.appendChild(text);
};