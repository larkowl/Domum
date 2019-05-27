let slider = document.getElementById('slider');
let slider_button_left = document.getElementById('slider-button-left');
let slider_button_right = document.getElementById('slider-button-right');
let min_position = -8;
let max_position = 0;
let screen_width = document.documentElement.clientWidth;
document.querySelectorAll('#slider>img').forEach(function(element) {max_position += element.offsetWidth + 5;})
slider.style.width = `${max_position + 1}px`;
slider_button_right.style.left = `${screen_width - 100}px`;
window.addEventListener('resize', function() {
	screen_width = document.documentElement.clientWidth;
	slider_button_right.style.left = `${screen_width - 100}px`;
});
const SLIDE = 900;

function sliderMoveLeft()
{
	if (min_position >= -8)
	{
		return;
	}
	if (min_position > -SLIDE - 8)
	{
		min_position = -SLIDE - 8;
	}
	min_position += SLIDE;
	slider.style.left = `${min_position}px`;
}

function sliderMoveRight()
{
	if (min_position - screen_width <= -max_position)
	{
		return;
	}
	if (min_position - screen_width < -max_position + SLIDE)
	{
		min_position = -max_position + screen_width + SLIDE;
	}
	min_position -= SLIDE;
	slider.style.left = `${min_position}px`;
}

slider_button_left.addEventListener('click', sliderMoveLeft);
slider_button_right.addEventListener('click', sliderMoveRight);