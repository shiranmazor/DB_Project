// assumption: dropdown names are "screen_name_1", "screen_name_2"

/*function validateSelection() {
    if (document.forms.selection.screen_name_1.value == document.forms.selection.screen_name_2.value) {
        alert('Warning: chose same person twice');
        document.forms.selection.submit.disabled = true;
    }
    else {
        document.forms.selection.submit.disabled = false;
    }
}
*/
function post(path, target, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("target", target);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);
            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

function generate_compare() {
    var left = document.forms.selection.screen_name_1.value;
    var right = document.forms.selection.screen_name_2.value;
    if (left != 'disabled' && right != 'disabled') {
        if (left == right) {
            alert('same person twice');
        }
        else {
            post('bottom', 'bottom', {screen_name_1: left, screen_name_2: right});
        }
    }

}

function refresh_bottom() {
    document.getElementById("bottom").src = document.getElementById("bottom").src;
}
function sleepFor( sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ }
}