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
			let content = {content: `<div class="info-title">${address}</div><br><div class="info-subtitle"><span>${to_metro} хвилин</span> від ст.м. <span>${station}</span></div>`};
			let info = new google.maps.InfoWindow(content);
			marker.addListener('click', function() {info.open(map, marker)});
		}
		else
		{
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}

let add_comment_button = document.getElementById('add_comment');
let add_comment_container = document.getElementById('add_comment_container');
let add_comment_cancel = document.getElementById('add_comment_cancel');
let add_comment_submit = document.getElementById('add_comment_submit');
let textarea = document.getElementById('comment_text');
let add_comment_slider = document.getElementById('comment_rate');
let add_comment_slider_result = document.getElementById('rate_value');

function displayRate()
{
    add_comment_slider_result.innerHTML = `&nbsp;&nbsp;&nbsp;${add_comment_slider.value}`;
}

function addComment()
{
  add_comment_container.style.display = 'grid';
}

function cancelComment()
{
  textarea.value = '';
  add_comment_slider.value = 5;
  add_comment_container.style.display = 'none';
}

function submitComment()
{
    document.getElementById('comment_text').value = textarea.value;
    document.getElementById('comment_rate_mine').value = add_comment_slider.value;
    document.getElementById('comment_form').submit();
	textarea.value = '';
    add_comment_slider.value = 5;
	add_comment_container.style.display = 'none';
}

add_comment_button.addEventListener('click', function() {addComment(); displayRate();});
add_comment_slider.addEventListener('input', displayRate);
add_comment_cancel.addEventListener('click', cancelComment);
add_comment_submit.addEventListener('click', submitComment);
