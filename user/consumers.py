from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Patient
from django.utils import timezone

class ChatPatientConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['UUCIpatient']
        self.room_group_name = 'chat_%s' % self.room_name
        self.patient = Patient.objects.get(pk= self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        isCli = text_data_json['isCli']

        # Intégration d'un nouveau message
        newMess = Message.objects.create(patient=self.patient, clinicien=self.patient.clinicienACharge, message=message, isClinicien=isCli)
        newMess.save()

        # recuperaption des anciens messages
        if isCli == None:
            query = Message.objects.filter(patient=self.patient)[:30]
            for message in query:
                self.send(text_data=json.dumps({
                    'isCli': query.isClinicien,
                    'message': query.message
                }))

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'isCli':isCli,
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        isCli = event['isCli']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'isCli': isCli,
            'message': message
        })
        )

