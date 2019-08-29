from django.urls import path
from user.ChannelChat import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:UUCIpatient>/', consumers.ChatPatientConsumer),
]