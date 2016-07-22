var ws = new WebSocket("ws://localhost:80/websocket");

ws.onopen = function() {
   ws.send("req");
};

ws.onmessage = function (evt) {
   var span = document.getElementById("snapshot"),
    text = document.createTextNode(''+evt.data);
	span.innerHTML = ''; // clear existing
	span.appendChild(text);
};