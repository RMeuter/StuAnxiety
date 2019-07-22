from django.urls import path
from . import views 
from django.views.generic.base import TemplateView

urlpatterns = [
    # Base vu par tous le monde
    path('', views.listModules, name='modules'),
    
    #Vue partie render
    path('<int:pk>', views.module, name='module'),
    path('AnalyseQuestionnaire/<int:pk>', views.questionnaireAnalyse, name='questionnaire'),
    
    ##### Vue des partie par Ajax
    path('sections/<int:module>/<int:ordre>', views.Sectiondetail.as_view(), name='section_form'),
    
    #####Reception des reponses par Ajax
    path('questionReceve/<int:pk>/<int:ordre>', views.ReceveQuestion.as_view()),
    
    #####Creation
    path('AlterModules', views.alterModules, name='AlterModules'),
    path('AlterPart', views.alterActivy, name='AlterPart'),

    path('AlterPart/<str:creation>/<str:typeActivity>/<int:pkActivity>/<int:ordreIn>', views.alterActivy, name='AlterPart'),
    
    #### Envoie et modification form
    path('showCreateForm/<str:formList>', views.EnvoieDifferentForm, name='callDiffFormForQuestion'),
    path('showCreateForm/<str:formList>/<int:pkModif>', views.EnvoieDifferentForm, name='callDiffFormForQuestion'),
    
              ]
