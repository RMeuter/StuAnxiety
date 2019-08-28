// Pour affiner avec ajax : https://www.tutorialspoint.com/django/django_ajax.htm


function affiche( module, ordre,nombreSection, retour) {
    /*
    integration fichier par : https://stackoverflow.com/questions/1999607/download-and-open-pdf-file-using-ajax
    */
    console.log(ordre);
    if(ordre==(nombreSection+1)){
        $(location).attr('href','/module/');
        return
    }
    $.ajax({
        url: 'sections/'+module+'/'+ordre,
        type: 'get',
        beforeSend: function(){
            $("#module").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');
        },
        success: function (data) {
            if(typeof(data) == "object"){
                if(data.video!=undefined && data.titre!=undefined) $('#module').html(video(data.titre,data.video));
                else if (data.text!=undefined) $('#module').html('<div class="col-12" type="text/html" width="720" height="720">'+data.text+"</div>");
                else {
                    $('#module').html(prepareQuestion(data.question));
                    $("#suivant").off("click");
                    $("#suivant").remove();
                    $("#envoie").click(function(){
                        envoieReponse(module, ordre,nombreSection,retour);
                    });
                }
            }
            $("#barre").attr("style", "width:"+Math.round(ordre*100/nombreSection)+"%");
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
      }
    });
    
    }

function video (titre, codeVideo){
    /*
    Prend un code vidéo issue de l'url youtube quand v=codeVideo
    */
    return '<h3 class="m-3 col-12 text-center">'+titre+'</h3><br/><iframe id="player" class="col-12" type="text/html" width="720" height="720" src="http://www.youtube.com/embed/'+codeVideo+'?enablejsapi=1&origin=http://example.com" frameborder="0"></iframe>';
}

function prepareQuestion(question){
    return "<form id='question' method='post' class='col-12 row' >"
        + "<div class='col-12' style='height: 100px;'>"
        + "<div class='form-group'>"
        + question
        + ""
        + "</div>"
        + "</div>"
        + "<div class='col-12' style='height: 100px;'>"
        + "<button class='btn btn-outline-dark float-none' id='envoie'>"
        + "Confirmer"
        + "</button>"
        + "</div>"
        + "</form>";
}

function envoieReponse(module, ordre, nombreSection, retour){
    $.post({
            url:'questionReceve/'+module+'/'+ordre,
            data:$("#question").serialize(),
            beforeSend: function(){
            $("#module").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');
            },
            success:function(data){
                if(data.valide==true){
                    ordre+=1;
                    $("#btn").html('<button id="suivant" class="btn btn-success offset-9 col-3">suivant</button>');
                    $("#suivant").on('click', function(){
                        passage(module, ordre, nombreSection, retour);
                    });
                    $("#suivant").click(function() {
                    if (ordre < nombreSection) {
                        ordre++;
                        affiche( module, ordre,nombreSection, retour);
                    }});
                    affiche( module, ordre,nombreSection, retour);
                } else {
                    affiche( module, ordre,nombreSection, retour);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });
}

function passage ( module,ordre,nombreSection, retour){
    if (ordre < (nombreSection)) {
        ordre++;
        affiche( module, ordre,nombreSection, retour);
    }     
    else if(ordre == (nombreSection)){
        ordre++;
        $('#suivant').text("Terminer");
        affiche( module, ordre,nombreSection, retour);
    } else {
        $(location).attr("href", retour);
    }
}
