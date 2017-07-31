/**
 * Created by JasonDeniega on 25/06/2017.
 */
$(function () {

    const errorText = $('#error-text');
    const errorText2 = $('#error-text-2');
    errorText.hide();
    errorText2.hide();

    $("#delete-button").click(deleteStall);
    $("#create-stall-button").click(createStall);
    $("#rename-stall-button").click(renameStall);
    $("#create-product-button").click(createProduct);
    $("#create-product-button-1").click(removeErrors);
    $("#create-product-button-2").click(removeErrors);


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

    function deleteStall() {
        //performs Ajax function to delete stall
        attachCSRF();
        $.ajax({
            url: window.location.pathname,
            method: "DELETE",
            success: function () {
                location.href = "/entity-management/";
            },
            error: function () {
                alert("something went wrong");
                location.href = "/entity-management/";
            }

        })

    }

    function createStall() {
        //performs Ajax function to create stall
        attachCSRF();
        const dict = {
            "stall_name": $("#stallname").val()
        };
        $.ajax({
            url: "/entity-management/stalls/",
            method: "POST",
            data: JSON.stringify(dict),
            success: function (data) {
                location.href = "/entity-management/stalls/" + data.id + "/";
            },
            error: function () {
                alert("something went wrong");
                location.href = "/entity-management/";
            }

        })

    }

    function renameStall() {
        //performs Ajax function to rename stall
        attachCSRF();
        dict = {
            "modified_name": $("#modified_stall_name").val()
        };
        $.ajax({
            url: window.location.pathname,
            method: "PUT",
            data: JSON.stringify(dict),
            success: function () {
                location.reload();
            },
            error: function () {
                alert("something went wrong");
                location.href = "/entity-management/";
            }

        })

    }

    function createProduct() {

        attachCSRF();

        const form = new FormData();

        const name = $("#create-product-name-input").val();
        const price = $("#create-product-price-input").val();
        const description = $("#create-product-description-input").val();
        const quantity = $("#create-product-quantity-input").val();
        const photo = $("#create-product-photo");

        form.append('photo', extractPhoto(photo));
        form.append('name', name);
        form.append('price', price);
        form.append('description', description);
        form.append('quantity', quantity);


        $.ajax({
            url: window.location.pathname + "products/",
            method: "POST",
            data: form,
            contentType: false,
            processData: false,
            success: () => {
                location.reload();
            },
            error: function (data) {
                displayErrors(data.responseJSON);
            }

        })

    }

    function displayErrors(errorArray) {

        if (errorArray.length == 0) {
            return;
        }

        const errorContainer = $('#create-product-errors');
        removeErrors();


        // errorText.show();

        errorArray.forEach((error) => {

            const errorBox = errorText.clone();
            const strong = errorBox.find('.error-strong-text');

            if (error) {
                strong.html(error);
            }
            errorContainer.append(errorBox);
            errorBox.show();

        });

    }

    function removeErrors() {
        $('#create-product-errors').html('');
    }

    function extractPhoto(input) {
        var files = input[0].files;
        if (!files.length) {
            alert('Unable to upload: no image/s selected');
            return false;
        }
        return files[0]
    }


});

const errorText2 = $("#error-text-2");
errorText2.hide();

function displayErrors(errorArray) {
    console.log(errorArray)
    if (errorArray.length == 0) {
        return;
    }

    const errorContainer = $('#edit-product-errors');
    removeErrors();


    // errorText.show();

    errorArray.forEach((error) => {

        const errorBox = errorText2.clone();
        const strong = errorBox.find('.error-strong-text');

        if (error) {
            strong.html(error);
        }
        errorContainer.append(errorBox);
        errorBox.show();
    });

}

function removeErrors() {
    $('#edit-product-errors').html('');
}

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

function extractPhoto(input) {
    const files = input[0].files;
    return files[0]
}

function editProduct(productID) {

    const form = new FormData();
    const name = $('#edit-product-name-input-' + productID).val();
    const description = $('#edit-product-description-input-' + productID).val();
    const price = $('#edit-product-price-input-' + productID).val();
    const photo = $('#edit-product-photo-' + productID);

    if (extractPhoto(photo)) {
        form.append('photo', extractPhoto(photo));
    }
    form.append('name', name);
    form.append('price', price);
    form.append('description', description);
    form.append('product_id', productID);

    attachCSRF();
    $.ajax({
        url: window.location.pathname + "products/update/",
        method: "POST",
        data: form,
        contentType: false,
        processData: false,
        success: function (data) {
        },
        error: function (data) {
            var new_array = [];
            var array = data["responseJSON"]["errors"];
            for(i=0;i<array.length;i++){
                new_array += array[i] + "\n"
            }
            alert(new_array);
        }

    })


}

function deleteProduct(productID){
        attachCSRF();
        const dict = {
            "product_id":productID
        };
        $.ajax({
            url: window.location.pathname + "products/",
            method: "DELETE",
            data: JSON.stringify(dict),
            success: function () {
                location.reload()
            },
            error: function () {
                location.reload()
            }

        })
    }

// function changeStatus(){
//     var stat = $('#order-status').val()
//     alert(stat);
//
//     const dict = {
//         "status": stat
//     };
//
//     $.ajax({
//         url: window.location.pathname + "status/",
//         method: 'GET',
//         data: JSON.stringify(dict),
//         success: function () {
//             location.reload()
//         },
//         error: function() {
//             alert("Yikes something went wrong")
//         }
//     })
//
// }