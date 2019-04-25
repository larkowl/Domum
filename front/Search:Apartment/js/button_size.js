window.addEventListener('resize', buttonSize);

function buttonSize()
{
	let screen_width = document.documentElement.clientWidth;
	let width = (screen_width - 116) / 4.5;
	let button = document.getElementById('submit');
	button.style.width = `${width}px`;
}