$(function () {
    
    //Ajout d'item
    $("#add").click(function () {
        let copie = $(".item:last").clone();
        nb++;
        copie.insertAfter(".item:last");
        $(".item:last").attr("id", nb);
        $(".item:last h5").text("Section numéro "+nb);
        $(".item:last imput:text").val("");
        $(".item:last textarea").html("");
        
    });
    /*
    Rendre l'ecriture plus visible !
    Et possbilité de déplcaement des modules
    $('input').focus(function(){
       $(this).parent().parent().parent().css("background-color","black") 
    });
    $('input').blur(function(){
       $(this).parent().parent().parent().css("background-color","white") 
    });
    */
});

function replaceNormal (){
    let nb=1;
    $.each($(".item"), function(){
        $(this).attr('id', nb);
        nb++;
    });
}

// Ajax a faire