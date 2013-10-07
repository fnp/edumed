(function($) {
    $(function() {


function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('__prefix__', total);
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id});
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('__prefix__', total);
        $(this).attr('for', newFor);
    });
    newElement.attr({'style': '', 'id': ''});
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).before(newElement);
}



            $('.add_more').click(function() {
                cloneMore($(this).data('selector'), $(this).data('prefix'));
            });

    });
})(jQuery);
