let ads = document.getElementById('ads');
let deals = document.getElementById('deals');
let tab1 = document.getElementById('tab1');
let tab2 = document.getElementById('tab2');

function switchToAds()
{
	deals.style.display = 'none';
	ads.style.display = 'block';
	tab1.style.borderBottom = '2px solid rgba(128, 0, 46, 1)';
	tab2.style.borderBottom = '2px solid transparent';
}

function switchToDeals()
{
	ads.style.display = 'none';
	deals.style.display = 'grid';
	tab2.style.borderBottom = '2px solid rgba(128, 0, 46, 1)';
	tab1.style.borderBottom = '2px solid transparent';
}

document.getElementById('tab1').addEventListener('click', switchToAds);
document.getElementById('tab2').addEventListener('click', switchToDeals);