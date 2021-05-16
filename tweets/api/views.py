from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetCreateSerializer
from tweets.models import Tweet


# Create your views here.
# not ModelViewSet 
class TweetViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to create, list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        overload create method, tweet.user should be current logged in user
        """
        serializer = TweetCreateSerializer(
            data = request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response({
                'sucess': False,
                'message':"Please check input",
                'errors': serializer.errors,
            }, status=400)
        # save will call method in TweetCreateSerializer
        tweet = serializer.save()
        return Response(TweetSerializer(tweet).data, status=201)

    def list(self, request, *args, **kwargs):

        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)

        tweets = Tweet.objects.filter(
            user_id = request.query_params['user_id']
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        return Response({'tweets': serializer.data})