from django.contrib.auth.models import User
from rest_framework import serializers
from cards.models import Card, Set


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['front', 'back']                  # Excluding group as it is assigned in views


class SetSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(read_only=True, view_name='set-detail')
    cards = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='card-detail')

    class Meta:
        model = Set
        fields = ['name', 'link', 'cards']      # Excluding owner as it is asigned in views

class UserSerializer(serializers.ModelSerializer):
    sets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'sets']