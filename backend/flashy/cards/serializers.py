from django.contrib.auth.models import User
from rest_framework import serializers
from cards.models import Card, Set


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['front', 'back']                  # Excluding group as it is assigned in views


class SetSerializer(serializers.ModelSerializer):
    cards = serializers.HyperlinkedIdentityField(view_name='set-card-list')

    class Meta:
        model = Set
        fields = ['name', 'cards']                  # Excluding owner as it is asigned in views

class UserSerializer(serializers.ModelSerializer):
    sets = serializers.PrimaryKeyRelatedField(many=True, queryset=Set.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'sets']