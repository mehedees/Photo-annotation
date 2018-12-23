function image_container(counter){
    var row = '<div class="col-xl-3 col-lg-3 col-md-3 col-sm-6 col-xs-6 current-uploads">';
    row = row + '<img class="img-thumbnail" id="current-upload'+counter+'"></div>';
    $('#current-uploads-container').append(row);
}

function get_image_faces(img){
    jQuery.ajax({
        url: "/generate-caption",
        type: "POST",
        // data: new FormData($('form')[0]),
        data: img,
        processData: false,
        contentType: false,
        beforeSend: function () {
            $("#caption").html("Please wait for result...");
        },
        success: function (response) {
            $("#caption").html(response);
        },
        error: function (data) {
            console.log(data.status);
        }
    });
}

$(document).ready(function () {
    $("#title-edit").click(function () {
        $('#album-title').hide();
        $('#title-edit').hide();
        $('#album-title-edit').show();
        $('#title-update').show();
    });
    $("#title-update").click(function () {
        $('#album-title').show();
        $('#title-edit').show();
        $('#album-title-edit').hide();
        $('#title-update').hide();
    });
    $("#desc-edit").click(function () {
        $('#album-desc').hide();
        $('#desc-edit').hide();
        $('#album-desc-edit').show();
        $('#desc-update').show();
    });
    $("#desc-update").click(function () {
        $('#album-desc').show();
        $('#desc-edit').show();
        $('#album-desc-edit').hide();
        $('#desc-update').hide();
    });

    $('.searched-photo').click(function () {
        $('#searched-photo-area').removeClass('col-xl-8 col-lg-8 col-md-8 col-sm-8 col-xs-8');
        $('#searched-photo-area').addClass('col-xl-6 col-lg-6 col-md-6 col-sm-4 col-xs-4');
        $('#search-section').removeClass('col-xl-4 col-lg-4 col-md-4');
        $('#search-section').addClass('col-xl-3 col-lg-3 col-md-3');
        $('#searched-photo-info').show();
    });
});
$(document).ready(function () {
    var counter = 1
    $('#photo-upload').change(function (event) {
        var numOfFiles = this.files.length;
        var output = document.getElementById('current-photo');
        output.src = URL.createObjectURL(this.files[0]);
        console.log("hgffgyhgf", new FormData($('form')));
        get_image_faces(new FormData($('form')[0]));
        for (i=0; i<numOfFiles; i++) {
            var output = document.getElementById('current-upload' + counter);
            output.src = URL.createObjectURL(this.files[i]);
            counter++;
            image_container(counter);
        }
    });
    $(document).on('click', '.current-uploads', function (event) {
        imgsrc = $(this).children('img').attr('src');
        console.log(imgsrc);
        var formData = new FormData();
        formData.append('photo', "blob:"+imgsrc, 'img.jpg');
        var output = document.getElementById('current-photo');
        output.src = imgsrc;
        //get_image_faces(formData);

        jQuery.ajax({
            url: "/change-caption",
            type: "POST",
            // data: new FormData($('form')[0]),
            data: imgsrc,
            processData: false,
            contentType: false,
            beforeSend: function () {
                $("#caption").html("Please wait for result...");
            },
            success: function (response) {
                $("#caption").html(response);
            },
            error: function (data) {
                console.log(data.status);
            }
        });


    });
});