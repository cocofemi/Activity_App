from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404

from activity.api.serializers import ActivitySerializer
from activity.models import Activity

class UserActivityList(generics.ListAPIView):
	serializer_class = ActivitySerializer

	def get_queryset(self):
		username = self.kwargs['username']
		return Activity.objects.filter(author__username=username)

class ActivityList(generics.ListAPIView):
	serializer_class = ActivitySerializer

	def get_queryset(self):
		pk = self.kwargs['pk']
		return Activity.objects.filter(id=pk)

class CreateActivity(generics.CreateAPIView):
	serializer_class = ActivitySerializer

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

