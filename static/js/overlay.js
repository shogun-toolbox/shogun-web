$(document).ready(function() {
	$(".overlay").click(function(event) {
		event.preventDefault();
		$('body').css('overflow', 'hidden');
		$(".overlay-content").load($(this).attr("href"),
			function() {
				$(".overlay-bg").fadeIn(500); 
			});
	});

	$(".overlay-close").click(function(event) {
		event.preventDefault();
		$(".overlay-bg").fadeOut(500, function() { $(".overlay-content").empty();});
		$('body').css('overflow', 'visible');
	});
});
