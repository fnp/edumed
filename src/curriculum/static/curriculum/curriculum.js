$(function() {
    if (typeof(curriculum_hide_form) != "undefined") {
        $('.curriculum-form form').hide();
        $('.curriculum-form h2 a span').show();
    }
    $('.curriculum-form h2 a').click(function() {
        $('.curriculum-form form').toggle('fast');
        $('span', this).toggle();
    });

    /* show togglers */
    $('.curriculum-section-toggler').show();

    $('.curriculum-section').each(function() {
        var category = this;

        /* set up togglers */
        $('.curriculum-section-toggler', this).click(function() {
            $('ul', category).toggle('fast');
        });

        /* set up section checkboxes */
        $('.s', category).change(function() {
            if ($(this).attr('checked')) {
                $('ul input', category).attr('checked', 'checked');
            }
            else {
                $('ul input', category).removeAttr('checked');
            }
        });

        /* unset section checkbox on unselect single competence */
        $('ul input', category).change(function() {
            if (!$(this).attr('checked')) {
                $('.s', category).removeAttr('checked', 'checked');
            }
        });

        /* hide unused section details on start */
        if ($('.s', category).attr('checked') || !$('ul input[checked]', category).length)
            $('ul', category).hide();
    });
});
