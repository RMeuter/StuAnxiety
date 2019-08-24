function graphique(pkVar, patient, listVar){
    
    $.get({
        url:"datasetDossier/"+patient+"/"+pkVar,
        beforeSend: function(){$("#chart").html('<div class="d-flex justify-content-center col-12 mb-5 mt-5 pt-5 pb-5"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>');},
        success:function(data){
            if(typeof(data.variable)=="object"){
                $("#chart").html("");
                var data =data.variable;
                var svg = dimple.newSvg("#chart", "100%", "100%");
                var chart = new dimple.chart(svg, data);
                
                var x =chart.addCategoryAxis("x", "Date");
                x.addOrderRule("Date");
                x.title= "Date de fin de module";	
                x.showGridlines = true;
                
                var y = chart.addMeasureAxis("y", "resultat");
                y.title= "Valeur de la variable selon chaque fin de module";
                y.fontSize = "12";	
                if(pkVar!=0){
                    // mise en forme de maximum, moyenne et min
                    y.overrideMin = listVar[pkVar].minVar;
                    y.overrideMax = listVar[pkVar].maxVar;
                }
                
                var s = chart.addSeries("Variable", dimple.plot.line);
                s.interpolation = "cardinal";
                chart.addLegend(60, 10, 500, 20, "right");
                chart.draw();
                        }
        },
        error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            },
        });
}


function SpiderGraphe(){
    //http://bl.ocks.org/nbremer/21746a9668ffdf6d8242
}