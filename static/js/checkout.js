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
            url: window.location.pathname,
            method: "DELETE",
            data: JSON.stringify(dict),
            success: function() {
                location.reload()
            },
            error: function() {
                alert("yikes! something went wrong");
                location.reload()
            }

        })
    }




