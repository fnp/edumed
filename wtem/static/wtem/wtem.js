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
            var exercise = el.data('exercise');
            if(exercise.get_answers) {
                push_answer(el, exercise.get_answers()[0]);
            }
        },

        open: function(el) {
            push_answer(el, el.find('textarea').val());
        }
    }

});