document.addEventListener('readystatechange', photosSize);
window.addEventListener('resize', photosSize);

function photosSize()
{
	let photos = document.querySelectorAll('.photo');
	let width = photos[0].offsetWidth;
	let height = width;
	photos.forEach(element => {
		element.style.height = `${height}px`;
	});
}