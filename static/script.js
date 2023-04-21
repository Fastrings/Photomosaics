function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('image-preview');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
};
function clearImage(event) {
    var preview = document.getElementById('image-preview');
    var form = document.getElementById('form');
    preview.src = null;
    form.reset();
};
function submitForm(event) {
    var im = document.forms["myForm"]["image"].value;
    var ts = document.forms["myForm"]["tile_size"].value;
    var me = document.forms["myForm"]["method"].value;
    var isValid = im != "" && ts != "" && me != "";
    if (isValid) {
        document.getElementById('form').submit();
        document.getElementById('form-btn').disabled = true;
        document.getElementById('spinner').style.visibility = 'visible';
    }
    else {
        var mess = [];
        mess.push("Some information is missing. More information below:")
        if (document.myForm.image.value === "") {
            mess.push("No image selected.")
        }
        if (document.myForm.tile_size.value === "") {
            mess.push("No tile_size selected.")
        }
        if (document.myForm.method.value === "") {
            mess.push("No method selected.")
        }
        alert(mess.join('\n\n'));
        return false;
    };
};

var perfEntries = performance.getEntriesByType("navigation");
if (perfEntries[0].type === "back_forward") {
    location.reload();
};