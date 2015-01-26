$(document).ready(function() {
	var latitude = $('.lat').html();
	latitude = parseFloat(latitude.replace(',', '.'));
	
	var longitude = $('.lon').html();
	longitude = parseFloat(longitude.replace(',', '.'));
	
	var map;
	var initialize;

	initialize = function(){
		var latLng = new google.maps.LatLng(latitude, longitude);
		var myOptions = {
			zoom      : 14,
			center    : latLng,
			mapTypeId : google.maps.MapTypeId.TERRAIN, //valeurs possible HYBRID, ROADMAP, SATELLITE, TERRAIN
			maxZoom   : 20
		};

		map = new google.maps.Map(document.getElementById('map1'), myOptions);
	};

	initialize();

});