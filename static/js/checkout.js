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

function recalculateTotal() {
    let totalPrice = 0;

    $('.line-item-row').get().forEach((item) => {
       const lineItem = $(item);
       const unitPrice = $(lineItem.find('.unit-price')[0]).val();
       const quantity = $(lineItem.find('.line-item-quantity-input')).val();

       console.log(unitPrice);
       console.log(quantity);

       if(quantity <= 0) {
           lineItem.remove();
           return;
       }

       const linePrice = unitPrice * quantity;

       $(lineItem.find('.line-price')).html("₱" + linePrice);
       totalPrice += linePrice;
    });

    if (totalPrice <= 0) {
        location.reload();
    }

    $('#cart-total-price').html("₱" + totalPrice);
}


$(() => {

    $('.line-item-quantity-input').each(function () {

        const quantityInput = $(this);

        quantityInput.bind('keyup input', () => {

            const productIDInput = $(this).parent().find('.line-item-product-id')[0];
            const productID = $(productIDInput).val();
            const newQuantity = quantityInput.val();

            const pair = {
                "product_id": productID,
                "quantity": newQuantity
            };

            attachCSRF();
            $.ajax({
                url: window.location.pathname,
                method: 'POST',
                data: JSON.stringify(pair),
                success: recalculateTotal,
            })


        });
    });
});

