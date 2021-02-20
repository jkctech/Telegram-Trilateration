// Default icons
var icon_user = L.icon({
	iconUrl: 'assets/user.png',
	iconSize: [32, 40],
	iconAnchor: [16, 40],
	popupAnchor: [0, -32]
});

var icon_group = L.icon({
	iconUrl: 'assets/group.png',
	iconSize: [32, 40],
	iconAnchor: [16, 40],
	popupAnchor: [0, -32]
});

// Generate circle with popup and center marker
function getCircle(lat, lon, circle_radius, color)
{
	var circle = L.circle([lat, lon], {
		color: color,
		fillColor: color,
		fillOpacity: 0.2,
		radius: circle_radius
	}).bindPopup(
		"<strong>Lat:</strong> " + lat + "<br>" +
		"<strong>Lon:</strong> " + lon + "<br>" +
		"<strong>Radius:</strong> " + circle_radius + " m"
	);
	var marker = L.circle([lat, lon], {
		color: color,
		fillColor: color,
		fillOpacity: 1,
		radius: 20
	});
	return [circle, marker];
}

// Generate a layer with all elements of a user
function getUserLayer(circles, location, color, name, type)
{
	var clist = [];
	var mlist = [];

	if (set_circles)
		circles.forEach(function(circle, index){
			var c = getCircle(circle['lat'], circle['lon'], circle['circle_radius'], color);
			clist.push(c[0]);
			clist.push(c[1]);
		});

	if (set_markers && location != false)
	{
		if (type == "User")
			var icon = icon_user;
		else
			var icon = icon_group;
		mlist.push(L.marker(location, {icon: icon}).bindPopup("<strong>[" + type.toUpperCase() + "]</strong></br>" + name));
	}

	var layer = L.layerGroup(clist.concat(mlist));
	
	return {
		"layer": layer,
		"circles": clist,
		"markers": mlist,
	};
}

// Base background layer
var map_base = L.tileLayer(map_url, {id: 'mapbox/light-v9', tileSize: 512, zoomOffset: -1, attribution: map_attr});

// Map initialization
map = L.map('map', {
	center: center,
	zoom: 8,
	layers: [map_base]
});

// Background layers
var bglayers = {
	"Grayscale": map_base,
	"Streets": L.tileLayer(map_url, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: map_attr})
};

// Add background and user layers
var layercontrol = L.control.layers(bglayers, [], {collapsed:false,sortLayers:true}).addTo(map);
