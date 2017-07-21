$(() => {
    var currentDate = new Date();
    var month = currentDate.getMonth() + 1;
    var day = currentDate.getDate();
    var year = currentDate.getFullYear();

    var string = "" + year;

    if (month < 10)
        string += "-0" + month;
    else
        string += "-" + month;

    if (day < 10)
        string += "-0" + day;
    else
        string += "-" + day;

    $('.form-group > input').attr('value', string);
    console.log(string);
});