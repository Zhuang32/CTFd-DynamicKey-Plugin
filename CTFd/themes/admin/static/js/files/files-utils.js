function updatefiles(){
    var chal = $('#files-chal').val();
    var form = $('#update-files form')[0];
    var formData = new FormData(form);
    $.ajax({
        url: script_root + '/admin/files/'+chal,
        data: formData,
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        success: function(data){
            form.reset();
            loadfiles(chal);
        }
    });
}

function loadfiles(chal, cb){
    $('#update-files form').attr('action', script_root+'/admin/files/'+chal)
    $.get(script_root + '/admin/files/' + chal, function(data){
        $('#files-chal').val(chal);
        var jsondata = $.parseJSON(JSON.stringify(data));
        var files = jsondata['files'];
        $('#current-files').empty();
        for(var x = 0; x < files.length; x++){
            var filename = files[x].file.split('/');
            var filename = filename[filename.length - 1];

            var curr_file = '<div class="col-md-12"><a href="{2}/files/{3}">{4}</a> <i class="btn-fa fas fa-times float-right" onclick="deletefile({0}, {1}, $(this))" value="{2}" ></i></div>'.format(
                chal,
                files[x].id,
                script_root,
                files[x].file,
                filename
            );

            $('#current-files').append(curr_file);
        }

        var file_generators = jsondata['file_generators'];
        $('#current-file-generators').empty();
        for(var x = 0; x < file_generators.length; x++){
            var filename = file_generators[x].file.split('/');
            var filename = filename[filename.length - 1];

            var curr_file = '<div class="col-md-12"><a href="{2}/files/{3}">{4}</a> <i class="btn-fa fas fa-times float-right" onclick="deletefile({0}, {1}, $(this))" value="{2}" ></i></div>'.format(
                chal,
                file_generators[x].id,
                script_root,
                file_generators[x].file,
                filename
            );

            $('#current-file-generators').append(curr_file);
        }

        if (cb){
            cb();
        }
    });
}

function deletefile(chal, file, elem){
    $.post(script_root + '/admin/files/' + chal,{
        'nonce': $('#nonce').val(),
        'method': 'delete',
        'file': file
    }, function (data){
        if (data == "1") {
            elem.parent().remove();
        }
    });
}


$(document).ready(function () {
    $('.edit-files').click(function (e) {
        var chal_id = $(this).attr('chal-id');
        loadfiles(chal_id, function () {
            $('#update-files').modal();
        });
    });


    $('#submit-files').click(function (e) {
        e.preventDefault();
        updatefiles()
    });
});
