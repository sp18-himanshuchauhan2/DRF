# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import viewsets, status
from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors},
                status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            'status': True, 'message': 'user successfully registered...'}, status.HTTP_201_CREATED)

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)

        print(serializer.data)
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])

        if not user:
            return Response({'status': False, 'message': 'invalid credentials...'}, status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status': True, "message": 'login successfully', 'token': str(token)})


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        print(request.user)
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)
    
        # return Response({'message': 'This is a get request'})
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
        # return Response({'message': 'This is a post request'})
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

        # return Response({'message': 'This is a put request'})
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
        
        # return Response({'message': 'This is a patch request'})
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'person deleted...'})

        # return Response({'message': 'This is a delete request'})

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    #search method - filter...
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset

        if search:
            queryset = queryset.filter(name__startswith=search) 
            
        serializer = PeopleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)