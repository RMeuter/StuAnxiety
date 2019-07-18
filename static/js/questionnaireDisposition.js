$(function(){
    $('#SelectionPrincipal').change(function(){
        $('#ZoneForm').html(choixPrincipal[int($('#SelectionPrincipal').val())][1]);
    });
});

choixPrincipal=[["Texte et image",appelForm() ] , ["Question", appelSelection()] , ["Réponse libre", appelSelection()]];
choixQuestion=["Réponse à choix unique", "Réponse à choix multiple", "Réponse libre"];

listInput={
    "listInputOnePossiblity":["Bouton Radio", "Selection"],
    "listInputManyPossiblity":["Case à cocher", "Selection multiple"],
    "listInputFree":["Reponse gradué", "Texte libre"],
};

function appelSelection(){
    
}

function appelForm(){
    
}