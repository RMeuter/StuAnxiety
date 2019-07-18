// Pour affiner avec ajax : https://www.tutorialspoint.com/django/django_ajax.htm


function video (titre, codeVideo){
    /*
    Prend un code vidéo issue de l'url youtube quand v=codeVideo
    */
    return '<h3 class="m-3 col-12 text-center">'+titre+'</h3><br/><iframe id="player" class="col-12" type="text/html" width="720" height="720" src="http://www.youtube.com/embed/'+codeVideo+'?enablejsapi=1&origin=http://example.com" frameborder="0"></iframe>';
}




function affiche( module, ordre,nombreSection) {
    /*
    integration fichier par : https://stackoverflow.com/questions/1999607/download-and-open-pdf-file-using-ajax
    */
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
                    $("#suivant").remove();
                    $("#envoie").click(function(){
                        envoieReponse(module, ordre,nombreSection);
                    });
                }
            }
            $("#barre").attr("style", "width:"+Math.round(ordre*100/nombreSection)+"%");
           
        }});
    
    }



function prepareQuestion(question){
    
    return "<form id='question' method='post' class='col-12'><div class='col-12 form-group'>"+question+"</div><button class='offset-12 col-12 btn btn-outline-dark' id='envoie'>Confirmer</button></form>";
}

function envoieReponse(module, ordre, nombreSection){
    $.post({
            url:'questionReceve/M/'+module+'/'+ordre,
            data:$("#question").serialize(),
            beforeSend: function(){
            $("#module").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');
        },
            success:function(data){
                if(data.valide==true){
                    ordre+=1;
                    $("#btn").html('<button id="suivant" class="btn btn-success offset-9 col-3">suivant</button>');
                    $("#suivant").click(function() {
                    if (ordre < nombreSection) {
                        ordre++;
                        affiche(module,ordre,nombreSection);}});
                }
                    affiche(module,ordre,nombreSection);
            }
            });
}
