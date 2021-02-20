// Move back to center
$("#center").click(centerScreen);

// Enable all layers
$("#allon").click(function() {
	for (var layer in userlayers)
		map.addLayer(userlayers[layer]);
});

// Disable all layers
$("#alloff").click(function() {
	for (var layer in userlayers)
		map.removeLayer(userlayers[layer]);
});

// Update filename for custom file selector
$('#fileinput').change(function() {
	var input = document.getElementById('fileinput');
	if (!input.files)
	{
		alert("This browser does not support the 'files' property of file inputs.");
		return;
	}
	$("#filepath").html(input.files[0].name);
});

// Responsiveness
$(window).on("resize", function () {
	$("#map").height($(window).height());
	$("#map").width($(window).width());
	map.invalidateSize();
}).trigger("resize");

function centerScreen()
{
	if (allfeatures.length > 0)
	{
		var group = L.featureGroup(allfeatures);
		var bounds = group.getBounds();

		map.fitBounds(bounds);
	}
	else
		map.setView(center, 8);
}
