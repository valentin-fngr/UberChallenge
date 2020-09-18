import pytest
from channels.testing import WebsocketCommunicator
from routing import application
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async #Db interraction inside async code
from django.contrib.auth.models import Group


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

#Testing :

    # 1 ) can_connect_to_server : DONE
    # 2 ) can_send_message_to_server : DONE
    # 3 ) can_receive_message_from_server :  DONE
    # 4 ) can_broadcast_message_to_server : DONE
    # 5 ) can_receive_broadcasted_message_from_server : DONE
    # 6 ) test_can_join_driver_group : DONE
    # 6 ) test_can_join_customer_group : TODO <-
    # 7 ) test_can_create_trips : TODO

PASSWORD = "passw0rd!"

def create_user(
        username="test_user1",
        password=PASSWORD,
        first_name="test_name",
        last_name="test_test",
        group=None
    ):
    user = User.objects.create_user(username=username, password=password, first_name=first_name)
    if group:
        driver_group, created = Group.objects.get_or_create(name="driver")
        driver_group.user_set.add(user)
        print(Group.objects.all())
    return user


@pytest.mark.asyncio
@pytest.mark.django_db
class TestWebsocket:

    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application, "/trips/")
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_can_send_message_to_server(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application, "/trips/")
        connected, _ = await communicator.connect()
        #sending message
        message = {"type": "echo.message", "data": "this is a basic message"}
        await communicator.send_json_to(message)
        #receiving message
        response = await communicator.receive_json_from()
        assert response["data"] == message["data"]

        await communicator.disconnect()

    async def test_can_broadcast_message_to_group(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/trips/"
        )
        connected, _ = await communicator.connect()
        channel_layer = get_channel_layer()
        message = {
            "type" : "echo.message",
            "data" : "Message broadcasted to test only"
        }
        #send message to all channels in test group
        await channel_layer.group_send("test",message)
        #retrieve message
        response = await communicator.receive_json_from()
        assert response["data"] == message["data"]
        await communicator.disconnect()

    async def test_can_authenticate(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        user = await database_sync_to_async(create_user)() #using await with sync_to_async or code breaks
        #returing access token
        access = AccessToken.for_user(user)
        print("given access token \n")
        print(access, "\n")
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/trips/?{access}"
        )
        connected, _ = await communicator.connect()
        assert connected == True
        await communicator.disconnect()

    async def test_can_join_driver_group_on_create(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        channel_layer = get_channel_layer()
        print("creating driver ")
        driver = await database_sync_to_async(create_user)(username="test_2", group="driver")
        access = AccessToken.for_user(driver)
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/trips/?{access}"
        )
        connected, _ = await communicator.connect()
        message = {
            "type" : "echo.message",
            "data" : f"{driver.username} just joined the driver pool"
        }
        await channel_layer.group_send("driver", message)
        response = await communicator.receive_json_from()
        assert message["data"] == response["data"]
        await communicator.disconnect()
