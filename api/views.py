from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import status
from .models import Conversation, ConversationStatistics
from .serializers import ConversationStatSerializer, ConversationSerializer
from rest_framework.views import APIView
from django.core.management import call_command
import requests

def index(request):
    tag_to_monitor = 'your_tag_name'
    # conversations = fetch_conversations(tag_to_monitor)
    
    return JsonResponse({'conversations': 'test'})


@api_view(['POST'])
def bot_action(request):
    #respond to email
    bot_response = "Bot's response here"
    return Response({'response': bot_response})

@api_view(['POST'])
def login_view(request):
    #login 
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'message': 'Login failed'}, status=401)

@api_view(['POST'])
def logout_view(request):
    #logout
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.all()
    serializer = ConversationSerializer(conversations, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def generate_and_add_conversation(request):
    # Create a new conversation
    new_conversation = Conversation(
        name="New Conversation",  
        ai_message="AI response",
        human_message="User message",
        tags=["tag1", "tag2"],  
    )
    
    new_conversation.save()

    serializer = ConversationSerializer(new_conversation)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def conversation_stats(request):
    call_command('calc_stats')
    stats = ConversationStatistics.objects.all()
    data = [{'tag': stat.tag, 'count': stat.conversation_count} for stat in stats]

    return JsonResponse({'data': data})