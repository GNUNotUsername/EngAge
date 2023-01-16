# rest api stuff

from rest_framework import serializers
from account.models import Contact, Message, UserInterests, Interests

class ContactSerializer(serializers.Serializer):

    class Meta:
        model = Contact
        fields = ['id', 'user1', 'user2']

class MessageSerializer(serializers.Serializer):

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']

class UserInterestsSerializer(serializers.Serializer):

    class Meta:
        model = UserInterests
        fields = ['id', 'user', 'interest']

