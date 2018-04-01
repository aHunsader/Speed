var wsaddr = window.location.host;
var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
var path = window.location.pathname.replace(/\/$/, "");
var wsUri = ws_scheme + "://" + wsaddr + path + "/ws/";
var websocket;
var dataLineGraph = [];
var svg;

function setupWebSocket(){
	websocket = new WebSocket(wsUri);
	websocket.onopen = function(evt) {
		onOpen(evt)
	};
	websocket.onmessage = function(evt){
		onMessage(evt)
	};
}

function onOpen(evt){
	console.log("connected to websocket");
}

function onMessage(evt){
	var data = JSON.parse(evt.data);
	console.log(data)

	if(data.number == 1){
		$("#username1").html(data.username);
		$("#speed1").html("Speed: " + data.speed + " mph");
		$("#acceleration1").html("Acceleration: " + data.acceleration + " mph/s");
		$("#speed_limit1").html("Speed Limit: " + data.limit);
		$("#street1").html("Current Street: " + data.street);
	}
	else{
		$("#username2").html(data.username);
		$("#speed2").html("Speed: " + data.speed + " mph");
		$("#acceleration2").html("Acceleration: " + data.acceleration + " mph/s");
		$("#speed_limit2").html("Speed Limit: " + data.limit);
		$("#street2").html("Current Address: " + data.street);
	}

	console.log(data.type)

	if(data.type == "midpoint"){
		map.setCenter({lat: parseInt(data.m_lat), lng: parseInt(data.m_lng)});
	}

	if(data.maps && data.number == 1){
		console.log("maps1");
		marker.setPosition({lat: parseInt(data.latitude), lng: parseInt(data.longitude)});
	}
	else if(data.maps && data.number == 2){
		console.log("maps2");
		marker2.setPosition({lat: parseInt(data.latitude), lng: parseInt(data.longitude)});
	}

	if(data.banner != ""){
		$("#nav_banner").show();
		$("#banner").html(data.banner);
	}



}

window.addEventListener("load", setupWebSocket, false);