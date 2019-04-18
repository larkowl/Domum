window.addEventListener('resize', buttonSize);

const INDUSTRIALNIY = ['Індустріальна', 'Тракторний завод'];
const KIIVSKIY = ['Пушкінська', 'Київська', 'Архітектора Бекетова', 'Академіка Барабашова', 'Майдан Конституції'];
const MOSKOVSKIY = ['Академіка Павлова', 'Студентська', 'Героїв Праці', 'Захисників України'];
const NEMYSHLYANSKIY = ['Палац спорту', 'Армійська', 'Московський проспект', 'Імені О.С. Масельського'];
const NOVOBAVARSKIY = ['Холодна гора'];
const OSNOVYANSKIY = ['Проспект Гагаріна'];
const SLOBIDSKIY = ['Завод імені Малишева', 'Спортивна', 'Метробудівників'];
const HOLODNOGIRSKIY = ['Південний вокзал', 'Центральний ринок'];
const SHEVCHENKIVSKIY = ['Наукова', 'Ботанічний Сад', 'Держпром', 'Університет', '23 Серпня', 'Олексіївська', 'Історичний музей', 'Перемога'];
const DISTRICTS = [INDUSTRIALNIY, KIIVSKIY, MOSKOVSKIY, NEMYSHLYANSKIY, NOVOBAVARSKIY, OSNOVYANSKIY, SLOBIDSKIY, HOLODNOGIRSKIY, SHEVCHENKIVSKIY];

function displayPrice()
{
	let price = document.getElementById('suggested_price');
	price.style.display = 'block';
}

function displaySortSelection()
{
	let sort = document.getElementById('select_sort');
	if (sort.style.display == 'block')
		sort.style.display = 'none';
	else
		sort.style.display = 'block';
}

let rent_term = document.getElementById('rent_term');
let beds_count = document.getElementById('beds_count');
let extra_options = document.getElementById('extra_options');
let house = document.getElementById('type2');
let office = document.getElementById('type3');
let house_label = document.getElementById('type2_label');
let office_label = document.getElementById('type3_label');
let house_break = document.getElementById('house_break');
let garage = document.getElementById('extra_options2');
let garage_label = document.getElementById('extra_options2_label');

function renting()
{
	rent_term.style.display = 'block';
	beds_count.style.display = 'block';
	extra_options.style.display = 'none';
	house.style.display = 'none';
	house_label.style.display = 'none';
	office.style.display = 'inline-block';
	office_label.style.display = 'inline-block';
	house_break.style.display = 'none';
}

function buying()
{
	rent_term.style.display = 'none';
	beds_count.style.display = 'none';
	extra_options.style.display = 'block';
	house.style.display = 'inline-block';
	house_label.style.display = 'inline-block';
	office.style.display = 'none';
	office_label.style.display = 'none';
	house_break.style.display = 'block';
}

function houseGarage()
{
	if (house.checked == true)
	{
		garage.style.display = 'inline-block';
		garage_label.style.display = 'inline-block';
	}
	else
	{
		garage.style.display = 'none'
		garage_label.style.display = 'none'
	}
}

function buttonSize()
{
	let screen_width = document.documentElement.clientWidth;
	let width = (screen_width - 116) / 4.5;
	let button = document.getElementById('submit');
	button.style.width = `${width}px`;
}

function selectStations()
{
	let stations = [];
	for (let i = 0; i < DISTRICTS.length; i++)
	{
		let district = document.getElementById(`district${i + 1}`);
		if (district.checked == true)
		{
			for (let k = 0; k < DISTRICTS[i].length; k++)
			{
				stations.push(DISTRICTS[i][k]);
			}
		}
	}
	return stations;
}

function displayStations(stations)
{
	let size = stations.length;
	let prev_stations = document.querySelectorAll('.station');
	
	for (let k = 0; k < prev_stations.length; k++)
		prev_stations[k].remove();

	for (let i = 0; i < size; i++)
	{
		let input = document.createElement('input');
		let label = document.createElement('label');
		let br = document.createElement('br');
		let parent = document.getElementById('metro_stations');
		input.type = 'checkbox';
		input.name = 'station';
		input.className = 'station';
		input.id = `station${i + 1}`;
		label.className = 'station';
		label.for = `station${i + 1}`;
		label.innerHTML = stations[i];
		br.className = 'station';
		parent.appendChild(input);
		parent.appendChild(label);
		parent.appendChild(br);
	}
}