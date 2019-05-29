$(function () {
    alert(creation());
    $.ajax({
        url: 'sections/list',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (data == null) {
                $('#module').append('<div class="liste" class="row"><div class="liste" class="row"><div class="text-center col-12 item border m-3 p-3"><h5>Section numéro 1</h5></div></div></div>');
            }
            let mod = '';
            data.module.forEach(section => {
                mod += '<div class="text-center col-12 item border m-3 p-3 rounded"><h5>' + section.titre + '</h5><div class="row">';
                if (section.text != "") {
                    mod += '<div class="col-12">' + section.text + '</div>'
                }
                if (section.image.name != undefined) {
                    mod += '<img src="' + section.image.path + '" alt="' + section.image.name + '" />'
                }
                mod += '<button class="btn deleteBtn" data-id="' + section.id + '">Delete</button><button class="btn updateBtn" data-id="' + section.id + '">Update</button></div></div></div>';
            });
            $('#module').append('<div class="liste" class="row">' + mod + '</div>');
            $('.deleteBtn').each((i, elm) => {
                $(elm).on("click", (e) => {
                    suppression($(elm));
                });
            });
            $('.updateBtn').each((i, elm) => {
                $(elm).on("click", (e) => {
                    modification($(elm));
                });
            });
        }
    });
});

function creation() {
    $.ajax({
        url: `sections/create`,
        type: 'post',
        dataType: 'json',
        success: function (data) {
            let s = "";
            for (key in data) {
                s += data[key] + " ";
            }
            return s;
        }
    });
}

function suppression(sec) {
    sectionId = $(sec).data('id');
    $.ajax({
        url: `/section/delete/`+sectionId,
        type: 'post',
        dataType: 'json',
        success: function (data) {
            $(el).parents()[1].remove()
        }
    });
}

function modification(sec) {
    sectionId = $(sec).data('id');
    $.ajax({
        url: `sections/update/`+sectionId,
        type: 'post',
        dataType: 'json',
        success: function (data) {
            let s = "";
            for (key in data) {
                s += data[key] + " ";
            }
            return s;
        }
    });
}
