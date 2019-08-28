function affiche(module, ordre, nombreSection, retour) {
    /*
    * Variable :
    *   - module :
    *
    * */
    if (ordre == (nombreSection + 1)) {
        $(location).attr('href', retour);
        return
    } else {
        $.ajax({
            url: 'sections/' + module + '/' + ordre,
            type: 'get',
            beforeSend: function () {
                $("#module").html(
                    '<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5">' +
                    '<div class="spinner-border" role="status">' +
                    '<span class="sr-only">' +
                    'Loading...' +
                    '</span></div></div>'
                );
            },
            success: function (data) {
                if (typeof (data) == "object") {
                    if (data.video != undefined && data.titre != undefined)
                        $('#module').html(video(data.titre, data.video));
                    else if (data.text != undefined)
                        $('#module').html('<div class="col-12" type="text/html" width="720" height="720">' + data.text + "</div>");
                    else {
                        $('#module').html(
                            prepareQuestion(data.question, data.inputType)
                        );
                        $("#envoie").click(function () {
                            envoieReponse(module, ordre, nombreSection, retour);
                        });
                    }
                }
                $("#barre").attr("style", "width:" + Math.round(ordre * 100 / nombreSection) + "%");
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });
    }
}

function video(titre, codeVideo) {
    /*
    Prend un code vidéo issue de l'url youtube quand v=codeVideo
    */
    return '<h3 class="m-3 col-12 text-center">' + titre + '</h3><br/><iframe id="player" class="col-12" type="text/html" width="720" height="720" src="http://www.youtube.com/embed/' + codeVideo + '?enablejsapi=1&origin=http://example.com" frameborder="0"></iframe>';
}

function prepareQuestion(question, inputType) {
    $("#suivant").off("click");
    $("#suivant").remove();

    if ( inputType==2 || inputType == 3) {
        str = "<div class='form-check'>" +
            question + "</div>";
    } else {
        str = + "<div class='form-group'>"
        + question + "</div>";
    }
    alert(question);
    return "<form id='question' method='post' class='col-12 row'>"
        + str
        + "<button class='col-12 btn btn-outline-dark m-3' id='envoie'>"
        + "Confirmer"
        + "</button>"
        + "</form>";
}

function envoieReponse(module, ordre, nombreSection, retour) {
    $.post({
        url: 'questionReceve/' + module + '/' + ordre,
        data: $("#question").serialize(),
        beforeSend: function () {
            $("#module").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');
        },
        success: function (data) {
            if (data.valide == true) {
                ordre += 1;
                $("#btn").html('<button id="suivant" class="btn btn-success offset-9 col-3">suivant</button>');
                $("#suivant").on('click', function () {
                    passage(module, ordre, nombreSection, retour);
                });
                affiche(module, ordre, nombreSection, retour);
            } else {
                affiche(module, ordre, nombreSection, retour);
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

function passage(module, ordre, nombreSection, retour) {
    if (ordre < (nombreSection)) {
        ordre++;
        alert('En dessous du nbSec: '+ordre+" au niveau plus un");
        affiche(module, ordre, nombreSection, retour);
    } else if (ordre == (nombreSection)) {
        alert('Egale à nbSec');
        ordre++;
        $('#suivant').text("Terminer");
        affiche(module, ordre, nombreSection, retour);
    } else {
        $(location).attr("href", retour);
    }
}
