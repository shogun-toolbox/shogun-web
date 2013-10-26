$(document).ready(function() {
	$(".overlay").click(function(event) {
		event.preventDefault();
		$('body').css('overflow', 'hidden');
		$(".overlay-iframe").attr('src', $(this).attr("href"));
		$(".overlay-new").attr('href', $(this).attr("href"));
		$(".overlay-bg").fadeIn(500);
	});

	$(document).keyup(function(event) {
		if (event.keyCode == 27) {
			closeOverlay(event);
		}
	});

	$(".overlay-close").click(function(event) {
		closeOverlay(event);
	});
});


function closeOverlay(event) {
	event.preventDefault();
	$(".overlay-bg").fadeOut(500);
	$('body').css('overflow', 'visible');
}

