$(function() {
    "use strict";
    var textarea = $("*[data-max-length]");
    textarea.before('<p class="counter">Pozostało: <span id="count"></span></p>');
    function updateCount(){
        var max_chars = this.getAttribute('data-max-length');
        var $this = $(this);
        var remaining = max_chars - $this.val().length;
        $("#count").text(remaining);
        $this.prev().toggleClass('negative', remaining < 0);
    }
    textarea.on('input', updateCount);
    textarea.trigger('input');
});
