
var choixPrincipal=new Array(
    {label: "Texte et image",fonction:appelForm("text")}, 
    {label:"Question",fonction:appelSelection("Type de reponse à la question")}, 
    {label:"vidéo",fonction:appelForm("video")}
);

function appelSelection(choix){
    var srt='<div class="input-group mb-3"><div class="input-group-prepend"><label class="input-group-text" for="listInput">'+choix+'</label></div><select class="custom-select" id="listInput">';
    srt+='<option value="'+"radio"+'">Bouton Radio</option>';
    srt+='<option value="'+"selection"+'">Selection</option>';
    srt+='<option value="'+"checkbox"+'">Case à cocher</option>';
    srt+='<option value="'+"selectMultiple"+'">Selection multiple</option>';
    srt+='<option value="'+"reponseGradue"+'">Reponse graduée</option>';
    srt+='<option value="'+"reponseTextLibre"+'">Texte libre</option>';
    srt+='</select> </div>';
    srt+='<div id="formQuest"></div>';
    return srt;
}

function appelForm(str){
    $.get(
    {
        url:"showCreateForm/"+str,
        success:function(data){
            alert(data);
        }
    }  
    );
    return '';
}

$(function(){
    $('#SelectionPrincipal').change(function(){
        $('#ZoneForm').html(choixPrincipal[parseInt($('#SelectionPrincipal').val())]['fonction']);
        if(parseInt($('#SelectionPrincipal').val())==1){
            // When the value change for the section of listInput, he show the form who call in range one of the listInput
            $('#listInput').change(function(){        
               //Warning optiminsation !
                $('#formQuest').append(appelForm($('#listInput').val()));
            });
        }
    });
});