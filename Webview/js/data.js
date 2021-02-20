// Handle the "Upload" of a new file
function handleFile()
{
	// Check if supported
	if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
		alert('File API not fully supported in this browser.');
		return;
	}   
	
	var input = document.getElementById('fileinput');
	
	// Check supported
	if (!input.files)
	{
		alert("This browser does not support the 'files' property of file inputs.");
		return;
	}

	// Check if file given
	if (!input.files[0])
	{
		alert("Please select a file first.");
		return;
	}
	
	// Link file to FileReader
	fr = new FileReader();
	fr.onload = drawdata;
	fr.readAsText(input.files[0]);
}

// Draw data based off object data
function drawdata()
{
	var data = jQuery.parseJSON(fr.result);
	jsonraw = data;

	readSettings();

	// Loop over entries
	for (var name in data)
	{
		// Ignore existing names
		if (name in userlayers)
			continue;

		var item = data[name];
		var display = "[" + item.type.toUpperCase().charAt(0) + "] " + name;

		var layer = getUserLayer(
			item.circles,
			item.location,
			item.color,
			name,
			item.type
		);

		// Save
		userlayers[name] = layer['layer'];

		// For incomplete users
		if (layer['markers'].length == 0)
		{
			// Skip if needed
			if (!set_unresolvable)
				continue;
			
			// Apply styling
			display = '<span style="color:red">' + display + '</span>';
		}

		// Add to global list of elements so we can center properly
		allfeatures = allfeatures.concat(layer['markers']);

		userlayers[name].addTo(map);

		// Append layer
		layercontrol.addOverlay(layer['layer'], display);
	}

	// Reset inputfile
	$("#fileinput").val("");
	$("#filepath").html("Please select a file.");

	// Move screen
	centerScreen();
}

function readSettings()
{
	set_circles = $("#drawcircles").is(":checked");
	set_markers = $("#drawmarkers").is(":checked");
	set_unresolvable = $("#unresolvable").is(":checked");
}

// Apply settings (Duh)
function applySettings()
{
	readSettings();

	// Redraw all layers (Actually apply settings)
	for (var name in userlayers)
	{
		// Save state
		var enabled = map.hasLayer(userlayers[name]);

		// Delete layer
		userlayers[name].remove();
		layercontrol.removeLayer(userlayers[name]);

		// Prepare new layer names
		var item = jsonraw[name];
		var display = "[" + item.type.toUpperCase().charAt(0) + "] " + name;

		// Build new layer (With settings)
		var layer = getUserLayer(
			item.circles,
			item.location,
			item.color,
			name,
			item.type
		);

		// Save
		userlayers[name] = layer['layer'];

		// For incomplete users
		if (layer['markers'].length == 0)
		{
			// Skip if needed
			if (!set_unresolvable)
				continue;
			
			// Apply styling
			display = '<span style="color:red">' + display + '</span>';
		}

		// Add to global list of elements so we can center properly
		allfeatures = allfeatures.concat(layer['markers']);

		// Append layer
		layercontrol.addOverlay(layer['layer'], display);

		// Restore state
		if (enabled)
			userlayers[name].addTo(map);
	}
}