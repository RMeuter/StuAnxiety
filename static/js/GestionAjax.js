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

    //------------------------------------------------------
    $.get({
        url:"GetPatientGroupe/"+$("#groupe").val(),
        success: function(data){
            alert(data);
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
    for (var key in listPat){
        $("#"+nameList).append(buildList(listPat[key].user__first_name,listPat[key].user__last_name));
    }
    $("#"+nameList).append("<input type='submit' class='btn btn-primary'/>");


    $("#"+nameNoList).html('<input type="hidden" name="'+typeHidden
        +'" value="'+ pkhidden+'">'
    );
    alert(data.noListPatient);
    $("#"+nameNoList).append(data.noListPatient+"<input type='submit' class='btn btn-primary'/>");
}


function buildCheckbox(lastName, firstName, pk) {
    return '<div class="input-group">'
        + '<div class="input-group-prepend">'
        + '<div class="input-group-text">'
        + '<input type="checkbox" name="Patient" value="'+ pk +'">'
        +'</div>'
        +'</div>'
        +'<div class="form-control">'
        + firstName + lastName
        + '</div>' + '</div>';
}
function buildList(lastName, firstName) {
    return ' <li class="list-group-item">' + lastName + firstName + '</li>';
}