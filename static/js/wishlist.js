$(document).ready(function () {
    $('.wish-link').on('click', function () {
        if ($(this).hasClass('wished')) {
            $(this).removeClass('wished').attr('title', 'Add to Wishlist');
        }
        else {
            $(this).addClass('wished').attr('title', 'Remove from Wishlist');
        }
    });
});