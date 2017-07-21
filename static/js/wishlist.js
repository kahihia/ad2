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

$(() => {
    $('.wish-link').on('click', function () {
        if ($(this).hasClass('wished')) {
            const link = $(this).removeClass('wished');
            link.attr('title', 'Add this to my Wishlist');
            link.attr('data-original-title', 'Add this to my Wishlist');
            $('[data-toggle="tooltip"]').tooltip();

        }
        else {
            const link = $(this).addClass('wished');
            link.attr('title', 'Remove this from my Wishlist');
            link.attr('data-original-title', 'Remove this from my Wishlist');

            attachCSRF()
            $product_id = $(this).parent().find('.product-id-input').val();
            console.log($product_id)

            const dict = {
                "product_id": $product_id
            };

            $.ajax({
                url: window.location.pathname + "wishlist/",
                method: "POST",
                data: JSON.stringify(dict),
                success: function () {
                    alert("Product successfully added to your wishlist!")
                },
                error: function () {
                    alert("yikes! something went wrong");
                }

            })
        }
    });

    $('[data-toggle="tooltip"]').tooltip();
});

