# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView

from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    courses = {
        'course_name': 'python',
        'learn': ['flask', 'django', 'restapi', 'fastapi'],
        'course_provider': 'Himanshu'
    }

    if request.method == 'GET':
        print(request.GET.get('search'))
        print("You hit a GET method...")
        return Response(courses)
    
    elif request.method == 'POST':
        data = request.data
        print("*****")
        print(data)
        # print(data['name'])
        print("*****")
        print("You hit a POST method...")
        return Response(courses)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        # objs = Person.objects.all()
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PATCH': # it supports the partial update in the data
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'person deleted...'})
    
@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        # data = serializer.validated_data
        data = serializer.data
        print(data)
        return Response({'message': 'success'})

    return Response(serializer.errors)

class PersonAPI(APIView):
    def get(self, request):
        return Response({'message': 'This is a get request'})
    
    def post(self, request):
        return Response({'message': 'This is a post request'})
    
    def put(self, request):
        return Response({'message': 'This is a put request'})
    
    def patch(self, request):
        return Response({'message': 'This is a patch request'})
    
    def delete(self, request):
        return Response({'message': 'This is a delete request'})
