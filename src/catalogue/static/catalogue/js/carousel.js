(function($){
$(function() {


$("#catalogue-carousel-links").each(function() {
    $slides = $(this); 

    $slides.cycle({
        fx: 'fade',
        speed: 1000,
        timeout: 5000,
        pager: '#catalogue-carousel-switcher',
        pagerAnchorBuilder: function() {},
    });

    $("#catalogue-carousel-switcher li").each(function(i, e) {
        $("a", e).click(function(ev) {
            ev.preventDefault();
            $slides.cycle(i);
        });
    });

});


});
})(jQuery);
