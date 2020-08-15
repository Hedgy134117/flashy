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
        serializer = SetSerializer(sets, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """ Create a set"""
        # The user cannot create a set if they are not logged in
        if request.user.is_anonymous:
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetDetail(APIView):
    """
    List all cards in a specific set, or add a new card to the specified set, or change the name of the set
    """
    def get_set(self, pk):
        """ Get the set that groups the cards together using the set id """
        try:
            return Set.objects.get(id=pk)
        except Set.DoesNotExist:
            return Http404
    
    def check_if_owner(self, request, pk):
        if request.user != self.get_set(pk).owner:
            return False
        return True
    
    def get(self, request, pk):
        """ Get all the cards in a set """
        cards = self.get_set(pk)
        serializer = SetSerializer(cards, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, pk):
        """ Add a card to a set """
        hasPermission = self.check_if_owner(request, pk)        
        if not hasPermission:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = CardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(group=self.get_set(pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """ Change the name of the set """
        hasPermission = self.check_if_owner(request, pk)        
        if not hasPermission:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        _set = self.get_set(pk)
        serializer = SetSerializer(_set, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """ Delete the set """
        hasPermission = self.check_if_owner(request, pk)        
        if not hasPermission:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        _set = self.get_set(pk)
        _set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CardDetail(APIView):
    """
    Get a card's details, change them, or delete the card.
    """    
    def get_card(self, pk):
        """ Get a specific card in a set """
        try:
            return Card.objects.get(pk=pk)
        except:
            return Http404

    def check_if_owner(self, request, pk):
        if request.user != self.get_card(pk).group.owner:
            return False
        return True

    def get(self, request, pk):
        """ Get the card in the set """
        card = self.get_card(pk)
        serializer = CardSerializer(card, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        """ Edit the card in the set """
        hasPermission = self.check_if_owner(request, pk)        
        if not hasPermission:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        card = self.get_card(pk)
        serializer = CardSerializer(card, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """ Delete the card """
        hasPermission = self.check_if_owner(request, pk)
        if not hasPermission:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        card = self.get_card(pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)