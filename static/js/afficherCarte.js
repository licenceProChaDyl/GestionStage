$(document).ready(function() {
	var directionsDisplay;
	var directionsService = new google.maps.DirectionsService();
	var map;
	var latitude = $('.lat').html();
	latitude = parseFloat(latitude.replace(',', '.'));
	var longitude = $('.lon').html();
	longitude = parseFloat(longitude.replace(',', '.'));

	function initialize() {
		directionsDisplay = new google.maps.DirectionsRenderer();
		var latLng = new google.maps.LatLng(latitude, longitude);
		var pts2 = new google.maps.LatLng(48.9292195, 2.4957121);
		var myOptions = {
				zoom: 14,
//				mapTypeId : google.maps.MapTypeId.TERRAIN,
				center: latLng
		}
		map = new google.maps.Map(document.getElementById('map1'), myOptions);
		directionsDisplay.setMap(map);
	}

	function calcRoute() {
		var selectedMode = document.getElementById('mode').value;
		var request = {
				origin: latLng,
				destination: pts2,
				travelMode: google.maps.TravelMode[selectedMode]
		};
		directionsService.route(request, function(response, status) {
			if (status == google.maps.DirectionsStatus.OK) {
				directionsDisplay.setDirections(response);
			}
		});
	}

	google.maps.event.addDomListener(window, 'load', initialize);

});