/**
 * Created by keith on 7/25/17.
 */

$(() => {
    function makePrimary(button) {
        button.removeClass('btn-secondary');
        button.addClass('btn-primary')
    }

    function makeSecondary(button) {
        button.removeClass('btn-primary');
        button.addClass('btn-secondary')
    }


    $('.add-button').get().forEach((button) => {
        const addButton = $(button);
        const isAddInput = $(addButton.parent().parent().find('.add-selected-input'));

        addButton.click(() => {
            const subtractButton = $(addButton.parent().find('.subtract-button'));
            makeSecondary(subtractButton);
            makePrimary(addButton);
            isAddInput.val('1');
        })
    });

    $('.subtract-button').get().forEach((button) => {
        const subtractButton = $(button);
        const isAddInput = $(subtractButton.parent().parent().find('.add-selected-input'));

        subtractButton.click(() => {
            const addButton = $(subtractButton.parent().find('.add-button'));
            makeSecondary(addButton);
            makePrimary(subtractButton);
            isAddInput.val('0');
        })
    })
})