import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from communications.api.consumers.serializers import PrivateRoomChatMessageSerializer
from communications.models import PrivateChatRoom, PrivateRoomChatMessage
from police_app_pro.exceptions import ClientError

User = get_user_model()
class AdminChatConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = None
        self.room_id = None
        self.room_group_name = None
        self.user_id = None

        await self.accept()

    async def receive_json(self, content):
        print("AdminChatConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        room = content.get("room", None)
        message = content.get("message", None)
        images = content.get("images", None)
        page_number = content.get("page_number", None)

        try:
            if command == "join":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                print("CONTENT: PAGE NUMBER: " + str(room))

                self.user = await get_user(user_id)

                print(self.user.email)

                await self.join_room(room, user_id, page_number)

            elif command == "send":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: ROOM ID: " + str(room))
                print("CONTENT: MESSAGE: " + str(message))

                await self.send_room(content["room"], content["user_id"], content["message"], content["images"])
                # raise ClientError(422,"You can't send an empty message.")






        except ClientError as e:
            await self.handle_client_error(e)

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # leave the room
        print("Admin Chat Consumers: disconnect")
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception:
            pass

    async def handle_client_error(self, e):
        """
        Called when a ClientError is raised.
        Sends error data to UI.
        """
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return

    async def join_room(self, room_id, user_id, page_number):
        """
        Called by receive_json when someone sent a join command.
        """
        print("AdminChatConsumers: join_room")
        # is_auth = is_authenticated(self.user)

        try:
            room = await get_room_or_error(room_id)
        except ClientError as e:
            await self.handle_client_error(e)

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
                room.group_name,
                self.channel_name,
            )


        ## Store that we're in the room
        self.room_id = room.id
        payload = await get_room_chat_messages(room, page_number)

        payload = json.loads(payload)
        #new_page_number = await get_new_page_number(room, page_number)
        #num_connected_users = await get_num_connected_users(room_id)


        # await self.send_messages_payload(payload)
        # Instruct their client to finish opening the room
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "send_messages_payload",
                "messages": payload,
                #"connected_user_count": num_connected_users,
                #"new_page_number": new_page_number
            }
        )

    async def send_room(self, room_id, user_id, message, images):
            """
            Called by receive_json when someone sends a message to a room.
            """
            # Check they are in this room
            print("Admin Chat: send_room")

            try:
                room = await get_room_or_error(room_id)
            except ClientError as e:
                await self.handle_client_error(e)

            await self.channel_layer.group_add(
                room.group_name,
                self.channel_name
            )

            # self.room_id = room.id
            message_data = await create_public_room_chat_message(room_id, user_id, message, images)

            if message_data != None:
                payload = json.loads(message_data)
                # await self.send_messages_payload(payload)

                await self.channel_layer.group_send(
                    room.group_name,
                    {
                        "type": "chat.message",
                        "messages": payload,
                    }
                )
            else:
                raise ClientError(204, "Something went wrong retrieving the chatroom messages.")

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print("AdminChatConsumers: chat_message from user #")
        await self.send_json(
            {
                "messages": event["messages"],
            },
        )

    async def send_messages_payload(self, event):
        """
        Send a payload of messages to the ui
        """
        print("AdminChatConsumers: send_messages_payload. ")

        await self.send_json(
            {
                "messages": event['messages'],
            },
        )


@database_sync_to_async
def get_room_or_error(room_id):
    """
	Tries to fetch a room for the user
	"""
    try:
        room = PrivateChatRoom.objects.get(pk=room_id)
    except PrivateChatRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")
    return room


@database_sync_to_async
def connect_user(room_id, user_id):
    try:
        message_room = PrivateChatRoom.objects.get(id=room_id)
        if message_room != None:
            message_room.connect_user(user_id)
            count = len(message_room.connected_users.all())
            print(count)

        # return json.dumps(team_count)

    except PrivateChatRoom.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")



@database_sync_to_async
def get_room_chat_messages(room):
    try:
        qs = PrivateRoomChatMessage.objects.by_room(room).order_by('-timestamp')[:20]


        serializers = PrivateRoomChatMessageSerializer(qs, many=True)
        if serializers:
            data = serializers.data

            return json.dumps(data)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def create_public_room_chat_message(room_id, user_id, message, files):

    user_obj = User.objects.get(user_id=user_id)

    room_obj = PrivateChatRoom.objects.get(id=room_id)

    message = PrivateRoomChatMessage.objects.create(
        user=user_obj,
        room=room_obj,
        message=message
    )
    message.save()

    #if files != None:
    #    for file in files:
    #        file_file = base64_file(file['file'], file['file_name'], file['file_ext'])
    #        new_file = File.objects.create(name=file['file_name'], file=file_file, user=user_obj)
    #        message.files.add(new_file)
    #        message.save()

    try:
        qs = PrivateRoomChatMessage.objects.by_room(room_id).order_by('-timestamp')
        qs.order_by('id')
       # p = Paginator(qs, 20)

        serializers = PrivateRoomChatMessageSerializer(qs, many=True)
        if serializers:
            data = serializers.data
            return json.dumps(data)

    except PrivateRoomChatMessage.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


def is_authenticated(user):
    print("AUTH USER: ")
    print(user)
    if user.is_authenticated:
        return True
    return False


