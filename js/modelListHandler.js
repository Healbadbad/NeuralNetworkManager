var ws = new WebSocket("ws://localhost:80/modelList");

ws.onopen = function() {
	console.log("file listener connected!");
};


ws.onmessage = function (evt) {
	var fileList = evt.data.substring(1, evt.data.length-1).split(', ');
	var target = document.getElementById("model-list");
	for(var key in fileList) {
		var button = document.createElement('button');
		button.className = 'ui inverted button';
		button.innerHTML = fileList[key].substring(1, fileList[key].length-1);
		target.appendChild(button);
	}
};