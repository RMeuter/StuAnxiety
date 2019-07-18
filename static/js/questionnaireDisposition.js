$(function(){
    $('#SelectionPrincipal').change(function(){
        $('#ZoneForm').html(choixPrincipal[int($('#SelectionPrincipal').val())][1]);
        if(int($('#SelectionPrincipal').val())==2){
            // When the value change for the section of listInput, he show the form who call in range one of the listInput
            $('#listInput').change(function(){        
               //Warning optiminsation !
                $('#ZoneForm').html(listInput[int($('#listInput').val())][1]);
            });
        }
    });
});

var choixPrincipal=[
    ["Texte et image",appelForm()], 
    ["Question", appelSelection("Type de reponse à la question",listInput)] , 
    ["vidéo", appelForm()],
];

var listInput=[
    ["Bouton Radio", appelForm()],
    ["Selection", appelForm()],
    ["Case à cocher", appelForm()],
    ["Selection multiple", appelForm()],
    ["Reponse graduée", appelForm()],
    ["Texte libre", appelForm()]
              ];


function appelSelection(choix, listechoix){
    srt='<div class="input-group mb-3"><div class="input-group-prepend"><label class="input-group-text" for="listInput">Type de question</label></div><select class="custom-select" id="listInput">';
    let smallint=0
    for quest in listechoix:
        srt+=('<option value="'+smallint+'">'+quest[0] +'</option>');
        smallint++;
    srt+='</select></div>';
    return srt;
}

function appelForm(str){
    $.get(
    {
        url:"",
        success:function(){
            
        }
    }  
    );
}