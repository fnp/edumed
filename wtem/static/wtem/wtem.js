$(function() {

    var to_submit;

    $('form').submit(function() {
        //e.preventDefault();
        to_submit = {};
        spinner.show();

        $('.exercise-wtem').each(function() {
            var el = $(this);
            if(el.hasClass('exercise')) {
                handlers.edumed(el);
            } else {
                var type = el.attr('data-type');
                if(handlers[type]) {
                    handlers[type](el);
                }
            }
        });
        $('input[name=answers]').val(JSON.stringify(to_submit));
    });

    var push_answer = function(el, answer) {
        to_submit[el.attr('data-id')] = answer
    };

    var handlers = {
        edumed: function(el) {
            var exercise = el.data('exercise'),
                to_push = {},
                open_part;
            if(exercise.get_answers) {
                to_push.closed_part = exercise.get_answers()[0];
            }
            open_part = el.find('.open_part');
            if(open_part.length) {
                to_push.open_part = open_part.find('textarea').val();
            }

            push_answer(el, to_push);
        },

        open: function(el) {
            var textareas = el.find('textarea'),
                to_push;
            if(textareas.length === 1) {
                to_push = el.find('textarea').val();
            } else {
                to_push = [];
                textareas.each(function() {
                    var textarea = $(this);
                    to_push.push({'id': textarea.attr('data-field-id'), 'text': textarea.val()});
                });
            }
            push_answer(el, to_push);
        }
    };

    var sms_handler = function() {
        var textarea = $(this),
            label_suffix = textarea.parent().find('.label_suffix'),
            left = 140 - textarea.val().length,
            to_insert = '(pozostało: ' + left + ')';
        if(left < 0) {
            to_insert = '<span style="color:red">' + to_insert + '</span>';
        }
        label_suffix.html(to_insert);
    };

    $('#wtem_sms').change(sms_handler).keyup(sms_handler);

    var spinner = $('.wtem_spinner');
    spinner.hide();
});