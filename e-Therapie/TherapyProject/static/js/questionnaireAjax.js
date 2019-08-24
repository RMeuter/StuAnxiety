// Pour affiner avec ajax : https://www.tutorialspoint.com/django/django_ajax.htm



function affiche( question, ordre,nombreQuestion) {
    /*
    integration fichier par : https://stackoverflow.com/questions/1999607/download-and-open-pdf-file-using-ajax
    */
    alert(question+" "+ ordre+" "+nombreQuestion);
    if(ordre==(nombreQuestion+1)){
        alert("je me barre bdb");
        $(location).attr('href','home');
        
    } else {
    alert("pas entrez 2");
    $.get({
        //--------------------------------------
        url: 'questions/'+question+'/'+ordre,
        beforeSend: function(){
            $("#question").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');
        },
        //--------------------------------------
        success: function (data) {
            alert(data.question);
            if(data.question != undefined){
                $('#question').html(data.question);
                alert("pas entrez 1");
                $("#envoie").off("click");
                $("#envoie").on("click",function(){
                    alert("pourquoi ça rentre !");
                    envoieReponse(question, ordre,nombreQuestion);
                });
                if(ordre==nombreQuestion){
                $('#envoie').text("Terminer");
                }
                } else {
                    alert('ne rentre pas !');
                }
            }
           
        //--------------------------------------
        });
        //--------------------------------------
    }
}
    
    

function envoieReponse(question, ordre,nombreQuestion){
    alert("entrez 1 !");
    $.post({
            url:'questionReceve/Q/'+question+'/'+ordre,
            data:$("#formQuest").serialize(),
            beforeSend: function(){
            $("#question").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');
        },
            success:function(data){
                if(data.valide==true){
                    ordre+=1;
                    alert("entrez 2 !");
                    affiche(question,ordre,nombreQuestion);
            }
            }});
}
