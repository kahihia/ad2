/**
 * Created by JasonDeniega on 25/06/2017.
 */
$(document).ready(function () {

    $("#delete-button").click(function () {
        deleteStall();
    });
    $("#create-stall-button").click(function () {
        createStall();
    });
    $("#rename-stall-button").click(function () {
        renameStall();
    });
    $("#create-product-button").click(function () {
        createProduct();
    });


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

        console.log(name);
        console.log(price);
        console.log(description);
        console.log(quantity);
        console.log(extractPhoto(photo));

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
                alert(data["new_product"]+" created");
                location.reload()
            },
            error: function () {
                alert("something went wrong");
            }

        })

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