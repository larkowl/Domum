function initMap()
{
	let location = {lat: 49.993360, lng: 36.230126};
	let map_options = {center: location, zoom: 10};
	let container = document.getElementById('map');
	let map = new google.maps.Map(container, map_options);
	var geocoder = new google.maps.Geocoder();
    document.addEventListener('readystatechange', function() {
		geocodeAddress(geocoder, map);
	});
}

function geocodeAddress(geocoder, resultsMap) 
{
	let address = 'пр-т. Московський, 124';
	geocoder.geocode({'address': address}, function(results, status)
	{
		if (status == google.maps.GeocoderStatus.OK)
		{
			var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
			let latLng = new google.maps.LatLng(latitude, longitude);
			resultsMap.setCenter(latLng);
			resultsMap.setZoom(15);
			let marker = new google.maps.Marker({
				map: resultsMap,
				position: results[0].geometry.location
			});
			let content = {content: `<div class="info-title">${address}</div><br><div class="info-subtitle"><span>10 хвилин</span> від ст.м. <span>Завод ім.Малишева</span></div>`};
			let info = new google.maps.InfoWindow(content);
			marker.addListener('click', function() {info.open(map, marker)});
		} 
		else
		{
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}