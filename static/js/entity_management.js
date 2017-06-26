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

});