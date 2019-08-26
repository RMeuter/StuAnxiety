$(function(){
    envoieData("GetPatientClinicien/"+$( "#clinicien" ).val(), $( "#clinicien" ).val(), "Clinicien");
    $( "#clinicien" ).change(function() {
        envoieData("GetPatientClinicien/"+$( "#clinicien" ).val(), $( "#clinicien" ).val(), "Clinicien");
   });
    //############################################################### Groupe ###########################################################
    envoieData("GetPatientGroupe/"+$("#groupe").val(),$("#groupe").val(),"Population");
   $( "#groupe" ).change(function() {
       envoieData("GetPatientGroupe/"+$("#groupe").val(),$("#groupe").val(),"Population");
   });
});










// ############################################################# Fonction ##############################################################

function envoieData(url, val, type) {
    if (type=="Clinicien"){
        $.get({
            url:url,
            success: function(data){
                buildForm(data, 'noListPatientC', 'listPatientC',val, "Clinicien");
            }
        });
    } else {
         $.get({
            url:url,
            success: function(data){
            buildForm(data, 'noListPatientP', 'listPatientP',$( "#groupe" ).val(), "Population");
            }
         });
    }

}

function buildForm(data, nameNoList, nameList, pkhidden, typeHidden) {
    /*Variable :
    * - data selon la forme envoyer en ajax (Deux clés : listPatient -> qui est relier à l'objet en question ex: Clincien et noListPatient qui n'est pas relier à l'objet en question)
    *       La première clé contient une liste de personne liée qui va etre énuméré par un for et mis en forme par buildList qui crée chaque itération
    *       La second contient un str qui est formulaire préconssu par django et qui validera en retour les information envoyer par post.
    * - nameList est le nom de la div qui se fera affecter la premiere liste
    * - nameNoList est le nom du form qui se fera affecter le contenu du formulaire
    * - hiddenType est une variable envoyer par post pour affecter à l'objet en hidden input les patient selectionner
    * */
    var listPat = data.listPatient;
    var noListPat = data.noListPatient;
    var liststr = "";
    for (var key in listPat){
        liststr += buildList(listPat[key].user__first_name,listPat[key].user__last_name);
    }
    $("#"+nameList).html(
        liststr
    );
    $("#"+nameNoList).html('<input type="hidden" name="'+typeHidden
        + '" value="'+ pkhidden+'">'
        + noListPat
    );
}

function buildList(lastName, firstName) {
    return ' <li class="list-group-item">' + lastName + firstName + '</li>';
}