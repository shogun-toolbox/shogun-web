$(document).on("click", ".overlay", function(){
        event.preventDefault();
	$('body').css('overflow', 'hidden');
    $(".overlay-content").load($(this).attr("href"),
      function(){$(".overlay-bg").fadeIn(500); 

		  $.getScript("http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML");
	  
	  })
});

$(document).on("click", ".overlay-close", function(event) {
    event.preventDefault();
    $(".overlay-bg").fadeOut(500, function() { $(".overlay-content").empty();});
	$('body').css('overflow', 'visible');
});
