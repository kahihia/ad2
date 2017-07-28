$(document).ready(function () {

    // Disables the button if the passwords do not match.
    $('#re-type').on('input', function () {
        if ($('#password').val() != $('#re-type').val()) {
            $(this).addClass('form-control-danger').removeClass('form-control-success');
            $(this).parent().addClass("form-group has-danger").removeClass('has-success');
        }
        else if ($('#password').val() == $('#re-type').val()) {
            $(this).removeClass('form-control-danger').addClass('form-control-success');
            $(this).parent().removeClass("form-group has-danger").addClass('has-success');
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
        }
    });

});