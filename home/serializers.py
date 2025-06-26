from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username is already taken...')
            
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email is already taken...')
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name', 'id']

class PeopleSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    country = serializers.SerializerMethodField()
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        # fields = ['name', 'age']
        fields = '__all__' 
        # depth = 1

    def get_country(self, obj):
        return "Inida"
    
    def get_color_info(self, obj):
        if obj.color is None:
            return None
        return {
            'color_name': obj.color.color_name,
            'hex_code': '#000'
        }

    def validate(self, data):
        special_char = "!@#$%^&*()-+?_=,<>/"
        if any (ch in special_char for ch in data['name']):
            raise serializers.ValidationError('name cannot contain special chars...')
        
        if data.get('age') and data['age'] < 18:
            raise serializers.ValidationError('age should be greater than 18...')
        
        return data