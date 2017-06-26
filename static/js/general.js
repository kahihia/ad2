/**
 * Created by keith on 6/22/17.
 */

//File input name
$("input[type=file]").change(function () {
    const fieldVal = this.files[0].name;
    if (fieldVal != undefined || fieldVal != "") {
        $(this).next(".custom-file-control").attr('data-content', fieldVal);
        console.log(fieldVal);
    }
});