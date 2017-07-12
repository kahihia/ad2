// This is the JS for the waitlisting in Product Catalog

$(document).ready(function () {

    // This gets the div itself

    // This gets the name of the product
    var product_id = $('.card-purchase-div').children().first().next().next().val();

    // This gets the quantity of the product
    var product_quantity = $('.card-purchase-div').children().first().next().next().next().val();
    console.log(product_quantity);

    // This gets the quantity the user wants
    var input_quantity = $('.card-purchase-div').children().last().prev().val();
    console.log(input_quantity);

    if (parseInt(product_quantity) < parseInt(input_quantity)) {
        console.log("Exceeded")
    }

});