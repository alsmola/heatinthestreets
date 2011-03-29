var min_zoom = 13;
var max_zoom = 17;
var range = [0,0,0,0];
var current_heatmap;
var map;
var metros;

function getHeatmap(zoom, lat, lng, category_id, metro_id, renderHeat) {
	var sf = new google.maps.LatLng(lat, lng);
	var myOptions = {
	  zoom: zoom,
	  center: sf,
	  mapTypeId: google.maps.MapTypeId.ROADMAP,
	  disableDefaultUI: true
	};

    map = new google.maps.Map(document.getElementById("map"), myOptions);
    
	if (renderHeat) {	
		current_heatmap = new google.maps.ImageMapType({
			getTileUrl: function(tile, zoom) {
				base = 'http://' + location.host + '/tile/';
				color_scheme = 'classic';
				url = base + color_scheme +'/'+ zoom +'/'
				url += tile.x +','+ tile.y + '/' + category_id + '/' + metro_id + '.png';
				return url;
			},
			tileSize: new google.maps.Size(256, 256),
			opacity:1.0,
			isPng: true
		});
	
		map.overlayMapTypes.push(null);
		map.overlayMapTypes.setAt("0", current_heatmap);
	}
	var strictBounds = new google.maps.LatLngBounds(
	  new google.maps.LatLng(range[0], range[2]),
	  new google.maps.LatLng(range[1], range[3])
	);

	// Listen for the dragend event
	google.maps.event.addListener(map, 'dragend', function() {

	  if (strictBounds.contains(map.getCenter())) return;

	  // We're out of bounds - Move the map back within the bounds
	  var c = map.getCenter(),
		  x = c.lng(),
		  y = c.lat(),
		  maxX = strictBounds.getNorthEast().lng(),
		  maxY = strictBounds.getNorthEast().lat(),
		  minX = strictBounds.getSouthWest().lng(),
		  minY = strictBounds.getSouthWest().lat();

	  if (x < minX) x = minX;
	  if (x > maxX) x = maxX;
	  if (y < minY) y = minY;
	  if (y > maxY) y = maxY;

	  map.setCenter(new google.maps.LatLng(y, x));
	});

	// Limit the zoom level
	google.maps.event.addListener(map, 'zoom_changed', function() {
	  if (map.getZoom() < min_zoom) map.setZoom(min_zoom);
	  if (map.getZoom() > max_zoom) map.setZoom(max_zoom);
	  current_zoom = map.getZoom();
	});  
}


function getNeighborhoods(category_id, category_name) {
	$.getJSON('neighborhoods/', {'category_id':category_id}, function(data) {
		$('#stats_table').html('');
		$('#stats').show();
		$('#stats_title').html('Neighborhood density for <b>' + category_name + '</b>');
        
		for (index in data) {
		    var percent = Math.ceil(data[index][2] * 100);
		    $('#stats_table').append('<tr><td class="neighborhood">' + data[index][1]  +'</td><td class="progressBar"><div id="progressbar_' + data[index][0] + '"></div></td></tr>');
            $("#progressbar_" + data[index][0]).progressbar({ value: percent });
		}

	});	
}

function updateMap() {
    metro_id = $('#metro :selected').val().split('|')[0]
	category_id = $('#category').val();
	range = $('#metro :selected').val().split('|')[1].split(',').map(Number);
	getHeatmap(min_zoom, (range[1] + range[0])/2, (range[3] + range[2])/2, category_id, metro_id, true);
}

$(document).ready(function() {	
	i = 0;
	
	$('#category').change(function() {    
    	category_id = $(this).val();
    	metro_id = $('#metro').val().split('|')[0];
    	//getNeighborhoods(category_id, category_name);
    	getHeatmap(map.getZoom(), map.getCenter().lat(), map.getCenter().lng(), category_id, true);
    });
    
    $("#metro option:eq(2)").attr("selected", "selected");
    
    $('#metro').change(function() {    
        updateMap();
    });
    
    $('#footer-content').hide();
	$('#footer-expander').click(function () {
	    $('#footer-content').toggle();
	});
	
	$('#stats').hide();

	$('#stats_title').text('');	
});


