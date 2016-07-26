var ws = new WebSocket("ws://localhost:80/websocket");

ws.onopen = function() {
   // ws.send("req");
};

ws.onmessage = function (evt) {
	var target = document.getElementById("snapshot");
	var div = document.createElement('div');
	target.innerHTML = evt.data; // clear existing
	var elements = div.childNodes;
	// span.appendChild(text);
};