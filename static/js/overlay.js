$(document).on("click", ".overlay", function(){
        event.preventDefault();
    $(".overlay-content").load($(this).attr("href"),
      function(){$(".overlay-bg").fadeIn(500); })
});

$(document).on("click", ".overlay-close", function(event) {
    event.preventDefault();
    $(".overlay-bg").fadeOut(500, function() { $(".overlay-content").empty();});
});
