(function($){
$(function() {


function scrollTo(thing) {
    $('html, body').scrollTop($(thing).offset().top - $('#level-chooser').outerHeight());
}

function updateView() {
    var scrolltop = $(window).scrollTop();

    $('#level-chooser-place').each(function(i, el){
        if (scrolltop > $(el).offset().top) {
            $("#level-chooser").addClass("fixed");
        }
        else {
            $("#level-chooser").removeClass("fixed");
        }
    });

    $('.level-toc').each(function(i, el) {
        var $sect = $($(el).parent());
        var menu_top = $('#level-chooser').outerHeight();
        var menu_scrolltop = scrolltop + menu_top;

        if (menu_scrolltop + 2 >= $sect.offset().top && 
                menu_scrolltop < $sect.offset().top + $sect.outerHeight()) {
            $(el).addClass("fixed").css("top", Math.min(
                menu_top, 
                - scrolltop + $sect.offset().top + $sect.outerHeight() - $(el).outerHeight()
            ));
            $("#level-chooser a[href='#" + $sect.attr('id') + "']").addClass('active');
        }
        else {
            $(el).removeClass("fixed");
            $("#level-chooser a[href='#" + $sect.attr('id') + "']").removeClass('active');
        }
    });
}



$("#level-chooser a, .level-toc a").click(function(ev) {
    ev.preventDefault();
    scrollTo($(this).attr('href'));
});





updateView();
$(document).scroll(updateView);
if (window.location.hash) {
    scrollTo(window.location.hash);
}


});
})(jQuery);
