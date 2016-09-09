var ws = new WebSocket("ws://137.112.158.202:80/buildSocket");

ws.onopen = function() {
	console.log("Build Log connected!");
};

ws.onmessage = function (evt) {
	var target = document.getElementById("logFeed");
	var div = document.createElement('div');
	target.innerHTML = target.innerHTML + evt.data; // clear existing
	var elements = div.childNodes;
	target.scrollTop = target.scrollHeight;
};