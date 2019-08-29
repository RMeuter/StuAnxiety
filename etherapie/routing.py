from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import user.ChannelChat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
            URLRouter(
                user.ChannelChat.routing.websocket_urlpatterns
            )
    ),
})