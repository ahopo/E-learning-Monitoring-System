function myFunction(id) {
    let x = document.querySelector("#" + id);
    if (x.innerHTML == "Read description") {
        x.innerHTML = "Close desciption";

        $("#" + id).removeClass('badge-info');
        $("#" + id).addClass('badge-danger');
    } else {
        x.innerHTML = "Read description";
        $("#" + id).addClass('badge-info');
        $("#" + id).removeClass('badge-danger');
    }
}

$(document.getElementById("empid")).on('keypress', function (e) {
    if (e.which == 13) {        
        let path = window.location.href.split("?")
        window.location = path[0] + '?eid=' + document.getElementById("empid").value
        
        return false
    }
});


$(document).ready(
    function () {
        $('input:file').change(
            function () {
                if ($(this).val()) {
                    $('input:submit').attr('disabled', false);
                    // or, as has been pointed out elsewhere:
                    ('input:submit').removeAttr('disabled');
                }
            }
        );
    });

$('#customFile').on('change', function () {
    //get the file name
    let fileName = $(this).val();
    //replace the "Choose a file" label

    $(this).next('.custom-file-label').html(fileName.replace('C:\\fakepath\\', ''));
})
 

$('#exampleModal').on('shown.bs.modal', function (event) {
    let triggerElement = $(event.relatedTarget);
    console.log(triggerElement);
    val = triggerElement.attr('value').split('.');
    empname = val[1].split('(');
    id = val[0];
    
    document.getElementById('exampleModalLabel').textContent = empname[0];
    document.getElementById("val").value = id;
});

$('#exampleModalCenter').on('shown.bs.modal', function (event) {
    let triggerElement = $(event.relatedTarget);
    
    val = triggerElement.attr('value');
    data=val.split('---')
    course_title=data[1]
    courese_description=data[0]
    document.getElementById('modalparag').textContent=courese_description;
    document.getElementById('exampleModalLongTitle').textContent=course_title;
    
    
});

if($('#messagesid').is(":visible")){
       
    setTimeout(function() {
        $("#messagesid").remove();
    }, 5000);
}

