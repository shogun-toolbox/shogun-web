$(document).on("click", ".overlay", function(){
	event.preventDefault();
    $(".overlay-content").load("/static/notebooks/bss_audio.html",
      function(){$(".overlay-bg").fadeIn(500); })
});

$(document).on("click", ".overlay-close", function(event) {
    event.preventDefault();
    $(".overlay-bg").fadeOut(500, function() { $(".overlay-content").empty();});
});
