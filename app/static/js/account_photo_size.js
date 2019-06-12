document.addEventListener('readystatechange', photoSize);
window.addEventListener('resize', photoSize);

function photoSize()
{
	let photo = document.getElementById('account_photo');
	let width = photo.offsetWidth;
	let height = width;
	photo.style.height = `${height}px`;
}