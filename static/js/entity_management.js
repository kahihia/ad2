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
    // $("#edit-product-button").click(populateProductModal);


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
                location.href = "/entity_management/";
            },
            error: function () {
                alert("something went wrong");
                location.href = "/entity_management/";
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
            url: "/entity_management/stalls/",
            method: "POST",
            data: JSON.stringify(dict),
            success: function () {
                alert(dict["stall_name"] + " created");
                location.href = "/entity_management/";
            },
            error: function () {
                alert("something went wrong");
                location.href = "/entity_management/";
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
            success: function (data) {
                alert(data["old_name"] + " successfully renamed to " + data["new_name"]);
                location.href = "/entity_management/";
            },
            error: function () {
                alert("something went wrong");
                location.href = "/entity_management/";
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
            success: function (data) {
                alert(data["new_product"] + " created");
                location.reload();
            },
            error: function (data) {
                displayErrors(data.responseJSON);
            }

        })

    }

    function populateProductModal() {
        console.log(window.location.pathname);
        attachCSRF();
        dict = {
            "product_id": $("#product-id")
        };

        $.ajax({
            url: window.location.pathname +"products/",
            method: "GET",
            data: JSON.stringify(dict),
            success: function (data) {
                console.log(data["name"]);
            },
            error: function () {
                alert("something went wrong");
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


})
;