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
<<<<<<< HEAD
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
=======

        const wishLink = $(this);

        if (wishLink.hasClass('wished')) {


            const productID = $(wishLink.parent().find('.product-id-input')[0]).val();

            attachCSRF();
            //Perform ajax
            $.ajax({
                url: '/product-catalog/wish/' + productID + '/',
                method: 'POST',
                success: () => {
                    alert("SUCCESS");
                    //Perform visual changes
                    const link = wishLink.removeClass('wished');
                    link.attr('title', 'Add this to my Wishlist');
                    link.attr('data-original-title', 'Add this to my Wishlist');
                }
            });

        }
        else {

            const productID = $(wishLink.parent().find('.product-id-input')[0]).val();

            attachCSRF();
            //Perform ajax
            $.ajax({
                url: '/product-catalog/wish/' + productID + '/',
                method: 'POST',
                success: () => {
                    //Perform visual changes
                    const link = wishLink.addClass('wished');
                    link.attr('title', 'Remove this from my Wishlist');
                    link.attr('data-original-title', 'Remove this from my Wishlist');
                }
            });


>>>>>>> 39dbd9371648af39afee79b0a1065e31cb276e92
        }
    });

    $('[data-toggle="tooltip"]').tooltip();
});

