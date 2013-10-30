$(function() {

    $('#submit_answers').click(function() {
        var to_submit = [];
        $('.exercise').each(function() {
            var exercise = $(this).data('exercise');
            if(exercise.get_answers) {
                to_submit.push(exercise.get_answers()[0]);
            }
        });
        console.log(JSON.stringify(to_submit));
    });

});