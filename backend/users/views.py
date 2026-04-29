from django.shortcuts import render
## backend/users/views.py

from rest_framework.viewsets import ModelViewSet
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all().order_by('-created_at')
    serializer_class = PersonSerializer
# Create your views here.
