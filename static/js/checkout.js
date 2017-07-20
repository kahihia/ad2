/**
 * Created by kamillegamboa on 18/07/2017.
 */

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

function removeProduct(productID) {
    attachCSRF();
    const dict = {
        "product_id": productID
    };
    $.ajax({
        url: window.location.pathname,
        method: "DELETE",
        data: JSON.stringify(dict),
        success: function () {
            location.reload()
        },
        error: function () {
            alert("yikes! something went wrong");
            location.reload()
        }

    })
}


$(() => {

    $('.line-item-quantity-input').each(function () {

<<<<<<< HEAD
        })
    }
$(document).ready(function(){

    $()

=======
        const quantityInput = $(this);

        quantityInput.bind('keyup input', () => {

            const productIDInput = $(this).parent().find('.line-item-product-id')[0];
            const productID = $(productIDInput).val();
            const quantity = quantityInput.val();

            const pair = {
                "product_id": productID,
                "quantity": quantity
            };

            attachCSRF();
            console.log(window.location.pathname)
            $.ajax({
                url: window.location.pathname,
                method: 'POST',
                data: JSON.stringify(pair),
                error: () => {
                    location.reload();
                },
            })


        });
    });
>>>>>>> adc0b3033784b42845f8433e16f228db8ba3dbb7
});

