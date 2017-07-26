$(document).ready(function () {
    $('#sign-in-button').on('click', function () {
        if ($('#password').val() != $('#re-type').val()) {
            alert('Passwords do not match!');
        }
    });
});