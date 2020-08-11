from cards.models import Card, Set
from cards.serializers import CardSerializer, SetSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class SetList(APIView):
    """
    List all sets, or start a new set
    """
    def get(self, request):
        """ List all sets """
        sets = Set.objects.all()
        serializer = SetSerializer(sets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """ Create a set"""
        # The user cannot create a set if they are not logged in
        if request.user.is_anonymous:
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardList(APIView):
    """
    List all cards in a specific set, or add a new card to the specified set
    """
    def get_set(self, pk):
        """ Get the set that groups the cards together using the set id """
        try:
            return Set.objects.get(id=pk)
        except Set.DoesNotExist:
            return Http404

    def get(self, request, pk):
        """ Get all the cards in a set"""
        cards = self.get_set(pk).cards
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        """ Add a card to a set """
        # The user cannot add a card to the set if they are not the same user who made the set
        if request.user != self.get_set(pk).owner:
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=self.get_set(pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)