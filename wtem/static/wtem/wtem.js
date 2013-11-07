$(function() {

    var to_submit;

    $('#submit_answers').click(function(e) {
        //e.preventDefault();
        to_submit = {};

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
        console.log(JSON.stringify(to_submit));
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
            open_part = el.find('.open_part')
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
    }

});