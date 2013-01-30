(function($){
$(function() {


$.fn.cycle.transitions.rgrowY = function($cont, $slides, opts) {
	opts.before.push(function(curr, next, opts) {
		$.fn.cycle.commonReset(curr,next,opts,true,false,true);
		opts.cssBefore.top = this.cycleH/2;
		opts.animIn.top = 0;
		opts.animIn.height = this.cycleH;
		opts.animOut.top = this.cycleH/2;
        opts.animOut.height = 0;
	});
	opts.cssBefore.height = 0;
	opts.cssBefore.left = 0;
};

$("#catalogue-carousel-links").each(function() {
    $(this).cycle({
        fx: 'rgrowY',
        sync:false,
        easeIn: 'easeInQuad',
        easeOut: 'easeOutQuad',
        speed: 1000,
        pager: '#catalogue-carousel-switcher',
        pagerAnchorBuilder: function(){},
    });
});


});
})($);
