$(document).ready(function () {
    $('.wish-button').on('click', function () {
        if ($(this).parent().parent().parent().hasClass('wished')) {
            $(this).parent().parent().parent().removeClass('wished').attr('title', 'Add to Wishlist');
        }
        else {
            $(this).parent().parent().parent().addClass('wished').attr('title', 'Remove from Wishlist');
        }
    });

    $('.wish-link').on('click', function () {
        if ($(this).parent().parent().hasClass('wished')) {
            $(this).parent().parent().removeClass('wished').attr('title', 'Add to Wishlist');
        }
        else {
            $(this).parent().parent().addClass('wished').attr('title', 'Remove from Wishlist');
        }
    });
});