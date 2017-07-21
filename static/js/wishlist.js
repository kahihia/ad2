$(() => {
    $('.wish-link').click(() => {
        if ($(this).hasClass('wished')) {
            $(this).removeClass('wished').attr('title', 'Add this to my Wishlist');
        }
        else {
            $(this).addClass('wished').attr('title', 'Remove this from my Wishlist');
        }
    });

    $('[data-toggle="tooltip"]').tooltip();
});