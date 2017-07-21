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
        }
    });

    $('[data-toggle="tooltip"]').tooltip();
});