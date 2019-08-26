$(function(){

     $.get({
        url:"GetPatientClinicien/"+$( "#clinicien" ).val(),
        success: function(data){
            buildForm(data, 'noListPatient', 'listPatient',$( "#clinicien" ).val(), "Clinicien");
        }
    });
    $( "#clinicien" ).change(function() {
    $.get({
        url:"GetPatientClinicien/"+$( "#clinicien" ).val(),
        success: function(data){
            buildForm(data, 'noListPatient', 'listPatient',$( "#clinicien" ).val(), "Clinicien");
        }
   });
   });

    //############################################################### Groupe ###########################################################
    $.get({
        url:"GetPatientGroupe/"+$("#groupe").val(),
        success: function(data){
            buildForm(data, 'noListPatient', 'listPatient',$( "#clinicien" ).val(), "Clinicien");
        }
          });



   $( "#groupe" ).change(function() {
       $.get({
        url:"GetPatientGroupe/"+$("#groupe").val(),
        success: function(data){
            $("#FormGroup").html(data+"<input type='submit' class='btn btn-primary'/>");
        }
          });
   });
});

Url = ["GetPatientGroupe/<int:pkPop>","GetPatientClinicien/<int:pkCli>" ]

function buildForm(data, nameNoList, nameList, pkhidden, typeHidden) {
    let listPat = data.listPatient;
    let noListPat = data.noListPatient;
    $("#"+nameList).html("");
    $("#"+nameNoList).html("");
    liststr = "";
    for (var key in listPat){
        liststr += buildList(listPat[key].user__first_name,listPat[key].user__last_name);
    }
    alert(liststr);
    $("#"+nameList).html(
        liststr
    );
    $("#"+nameNoList).html('<input type="hidden" name="'+typeHidden
        + '" value="'+ pkhidden+'">'
        + data.noListPatient
        + "<input type='submit' value='Valider' class='btn btn-primary'/>"
    );
}

function buildList(lastName, firstName) {
    return ' <li class="list-group-item">' + lastName + firstName + '</li>';
}