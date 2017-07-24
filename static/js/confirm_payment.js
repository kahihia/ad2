/**
 * Created by JasonDeniega on 21/07/2017.
 */

$(document).ready(function(){
    function confirmPaymentCustomer(){
        const form = new FormData();
        const photo = $('#edit-product-photo-' + productID);

    }
});

function attachCSRF() {
        const csrftoken = $.cookie('csrftoken');

        const csrfSafeMethod = function (method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        };

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

}
function extractPhoto(input) {
        var files = input[0].files;
        if (!files.length) {
            alert('Unable to upload: no file selected');
            return;
        }
        return files[0]
    }