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

        if ($('#username').hasClass('form-control-success')) {
            var username = true;
        }

        if ($('#password').hasClass('form-control-success')) {
            var password = true;
        }

        if ($('#re-type').hasClass('form-control-success')) {
            var retype = true;
        }

        if ($('#name').hasClass('form-control-success')) {
            var name = true;
        }

        if ($('#address').hasClass('form-control-success')) {
            var address = true;
        }

        if ($('#city').hasClass('form-control-success')) {
            var city = true;
        }

        if ($('#postal-code').hasClass('form-control-success')) {
            var postal = true;
        }

        if ($('#number').hasClass('form-control-success')) {
            var number = true;
        }
        if (username && password && retype && name && address && city && postal && number && matching) {
            $('#sign-in-button').removeClass('disabled').removeAttr('disabled');
        }

    });


});