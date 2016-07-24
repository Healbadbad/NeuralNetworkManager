var ws = new WebSocket("ws://localhost:80/modelList");

ws.onopen = function() {
	console.log("file listener connected!");
};

ws.onmessage = function (evt) {
	console.log(evt);
	var target = document.getElementById("model-list");
	var div = document.createElement('div');
	target.innerHTML = evt.data; // clear existing
	var elements = div.childNodes;
	// span.appendChild(text);
};