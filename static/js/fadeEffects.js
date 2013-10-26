// fadeEffects.js written By AdamKhoury.com

/*

  USAGE IS SIMPLE: fadeIn(elementID); fadeOut(elementID);

*/

var fade_in_from = 0;

var fade_out_from = 10;

function fadeIn(element){

	var target = document.getElementById(element);

	target.style.display = "block";

	var newSetting = fade_in_from / 10;

	target.style.opacity = newSetting;

	// opacity ranges from 0 to 1

	fade_in_from++;

	if(fade_in_from == 10){

		target.style.opacity = 1;

		clearTimeout(loopTimer);

		fade_in_from = 0;

		return false;

	}

	var loopTimer = setTimeout('fadeIn(\''+element+'\')',50);

}

function fadeOut(element){

	var target = document.getElementById(element);

	var newSetting = fade_out_from / 10;

	target.style.opacity = newSetting;

	fade_out_from--;

	if(fade_out_from == 0){

		target.style.opacity = 0;

		target.style.display = "none";

		clearTimeout(loopTimer);

		fade_out_from = 10;

		return false;

	}

	var loopTimer = setTimeout('fadeOut(\''+element+'\')',50);

}