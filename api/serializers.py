from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message="A user with that email address already exists.")]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        password = validated_data['password']
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPOST
        fields = ['ID','title', 'body']
        
        extra_kwargs = {
            'title': {'required': True},
            'body': {'required': True},
        }

    def create(self,validated_data):
        request = self.context.get("request")
        blogpost= BlogPOST()
        blogpost.auther=User.objects.get(id=request.user.id)
        blogpost.title=validated_data['title']
        blogpost.body=validated_data['body']
        blogpost.save()
        return blogpost


    


