$(document).ready( function() {
	var initialLocation;
	var siberia = new google.maps.LatLng(60, 105);
	var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);
	var browserSupportFlag =  new Boolean();
	var current_lat = $("#id_latitude").val()
	var current_lng = $("#id_longitude").val()

	function initialize() {
		var myOptions = {
			zoom: 5,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		geocoder = new google.maps.Geocoder();
		var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
		// Try W3C Geolocation (Preferred)
		if(navigator.geolocation) {
			browserSupportFlag = true;
			navigator.geolocation.getCurrentPosition( function(position) {
				initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
				detected_location = initialLocation;
				currentLocation = new google.maps.LatLng(current_lat,current_lng);
				var currentinfowindow = new google.maps.InfoWindow({
					content: 'Current set location'
				});
				var currentmarker = new google.maps.Marker({
					position: currentLocation,
					map: map
				});
				google.maps.event.addListener(currentmarker, 'click', function() {
					currentinfowindow.open(map,currentmarker);
				});
				
				var detectedinfowindow = new google.maps.InfoWindow({
					content: 'Detected location'
				});
				var marker = new google.maps.Marker({
					position: detected_location,
					map: map,
					draggable: true
				});
				google.maps.event.addListener(marker, 'click', function() {
					detectedinfowindow.open(map,marker);
				});
				google.maps.event.addListener(marker, 'dragend', function() {
					detected_location = marker.getPosition()
					// Search for place data
					geocoder.geocode( { 'location': detected_location}, function(results, status) {
						if (status == google.maps.GeocoderStatus.OK) {
							$("#id_country").val('');
							$("#id_location").val('');
							map.setCenter(detected_location);
							for(var addComponent in results[0].address_components) {
								var component = results[0].address_components[addComponent];
								for(typeIndex in component.types ) {
									if(component.types[typeIndex]=='country') {
										$("#id_country").val(component.short_name);
									}
									if(component.types[typeIndex]=='locality') {
										$("#id_location").val(component.short_name);
									}
								}
							}

							$("#id_latitude").val(results[0].geometry.location.lat().toFixed(6));
							$("#id_longitude").val(results[0].geometry.location.lng().toFixed(6));
						} else {
							alert("Geocode was not successful for the following reason: " + status);
						}
					});
				});
				map.setCenter(initialLocation);
				// map.setZoom(14);
			}, function() {
				handleNoGeolocation(browserSupportFlag);
			});
		} else {
			browserSupportFlag = false;
			handleNoGeolocation(browserSupportFlag);
		}

		function handleNoGeolocation(errorFlag) {
			if (errorFlag == true) {
				initialLocation = newyork;
			} else {
				initialLocation = siberia;
			}
			map.setCenter(initialLocation);
				detected_location = initialLocation;
				currentLocation = new google.maps.LatLng(current_lat,current_lng);
				var currentinfowindow = new google.maps.InfoWindow({
					content: 'Current set location'
				});
				var currentmarker = new google.maps.Marker({
					position: currentLocation,
					map: map
				});
				google.maps.event.addListener(currentmarker, 'click', function() {
					currentinfowindow.open(map,currentmarker);
				});
				
				var detectedinfowindow = new google.maps.InfoWindow({
					content: 'Detected location'
				});
				var marker = new google.maps.Marker({
					position: detected_location,
					map: map,
					draggable: true
				});
				google.maps.event.addListener(marker, 'click', function() {
					detectedinfowindow.open(map,marker);
				});
				google.maps.event.addListener(marker, 'dragend', function() {
					detected_location = marker.getPosition()
					// Search for place data
					geocoder.geocode( { 'location': detected_location}, function(results, status) {
						if (status == google.maps.GeocoderStatus.OK) {
							map.setCenter(detected_location);
							$("#id_country").val('');
							$("#id_location").val('');
							for(var addComponent in results[0].address_components) {
								var component = results[0].address_components[addComponent];
								for(typeIndex in component.types ) {
									if(component.types[typeIndex]=='country') {
										$("#id_country").val(component.short_name);
									}
									if(component.types[typeIndex]=='locality') {
										$("#id_location").val(component.short_name);
									}
								}
							}

							$("#id_latitude").val(results[0].geometry.location.lat().toFixed(6));
							$("#id_longitude").val(results[0].geometry.location.lng().toFixed(6));
						} else {
							alert("Geocode was not successful for the following reason: " + status);
						}
					});
				});
				map.setCenter(initialLocation);

		}

	}

	initialize();
});