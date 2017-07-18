/**
 * Created by kamillegamboa on 18/07/2017.
 */

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

    function removeProduct(productID) {
        attachCSRF();
        const dict = {
            "product_id":productID
        };
        $.ajax({
            url: window.location.pathname + "checkout_process/",
            method: "DELETE",
            data: JSON.stringify(dict),
            success: function(data) {
                console.log(data["name"]);
                location.reload()
            },
            error: function() {
                console.log(data["name"]);
                alert("yikes! something went wrong");
                location.reload()
            }

        })
    }

