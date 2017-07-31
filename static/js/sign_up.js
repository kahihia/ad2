$(document).ready(function () {

    var matching = true;
    $('#re-type').on('input', function () {
        if ($('#password').val() != $('#re-type').val()) {
            $(this).addClass('form-control-danger').removeClass('form-control-success');
            $(this).parent().addClass("form-group has-danger").removeClass('has-success');
            $('#sign-in-button').addClass('disabled').attr('disabled', 'disabled');
            matching = false;
        }
        else if ($('#password').val() == $('#re-type').val()) {
            $(this).removeClass('form-control-danger').addClass('form-control-success');
            $(this).parent().removeClass("form-group has-danger").addClass('has-success');
            matching = true;
        }
    });

    $('input.form-control').on('input', function () {
        if ($(this).val().length != 0) {
            $(this).addClass('form-control-success');
            $(this).parent().addClass("form-group has-success");
        }
        else {
            $(this).removeClass('form-control-success');
            $(this).parent().removeClass("form-group has-success");
            $('#sign-in-button').addClass('disabled').attr('disabled', 'disabled');
        }

        const username = $('#username').hasClass('form-control-success');
        const password = $('#password').hasClass('form-control-success');
        const retype = $('#re-type').hasClass('form-control-success');
        const name = $('#name').hasClass('form-control-success');
        const address = $('#address').hasClass('form-control-success');
        const city = $('#city').hasClass('form-control-success');
        const postal = $('#postal-code').hasClass('form-control-success');
        const number = $('#number').hasClass('form-control-success');

        if (username && password && retype && name && address && city && postal && number && matching) {
            $('#sign-in-button').removeClass('disabled').removeAttr('disabled');
        }

    });


});