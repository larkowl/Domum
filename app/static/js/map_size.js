document.addEventListener('readystatechange', mapSize);
window.addEventListener('resize', mapSize);

function mapSize()
{
	let map = document.getElementById('map');
	let width = map.offsetWidth;
	let height = width;
	map.style.height = `${height}px`;
}