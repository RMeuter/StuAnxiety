$(function(){
    $.get({
        url:"GetPatientClinicien/"+$( "#clinicien" ).val(),
        success: function(data){
            $("#FormCli").html(data+"<input type='submit' class='btn btn-primary'/>");
        }
          });



   $( "#clinicien" ).change(function() {
    $.get({
        url:"GetPatientClinicien/"+$( "#clinicien" ).val(),
        success: function(data){
            $("#FormCli").html(data+"<input type='submit' class='btn btn-primary'/>");
        }
          });
   });
    //------------------------------------------------------
    $.get({
        url:"GetPatientGroupe/"+$("#groupe").val(),
        success: function(data){
            $("#FormGroup").html(data+"<input type='submit' class='btn btn-primary'/>");
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