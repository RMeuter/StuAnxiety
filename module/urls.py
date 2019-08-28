from django.urls import path
from module.views import views_show_module, view_alter_module

urlpatterns = [
    # Base vu par tous le monde
    path('', views_show_module.listModules, name='modules'),
    
    #Vue partie render
    path('<int:pk>', views_show_module.module, name='module'),
    path('AnalyseQuestionnaire/<int:pk>', views_show_module.questionnaireAnalyse, name='questionnaire'),
    
    ##### Vue des partie par Ajax
    path('sections/<int:module>/<int:ordre>', views_show_module.Sectiondetail.as_view()),
    #####Reception des reponses par Ajax
    path('questionReceve/<int:pk>/<int:ordre>', views_show_module.ReceveQuestion.as_view()),
    
    #######################################################################################################################
    ##########################################Creation####################################################################
    #######################################################################################################################
    path('AlterModules', view_alter_module.alterModules, name='AlterModules'),
    path('AlterPart', view_alter_module.alterActivy, name='AlterPart'),
    path('AlterPart/<str:creation>/<str:typeActivity>/<int:pkActivity>/<int:ordreIn>', view_alter_module.alterActivy, name='AlterPart'),
    #### Envoie et modification form
    path('showCreateForm/<str:formList>', view_alter_module.EnvoieDifferentForm, name='callDiffFormForQuestion'),
    path('showCreateForm/<str:formList>/<int:pkModif>', view_alter_module.EnvoieDifferentForm, name='callDiffFormForQuestion'),
    
              ]
