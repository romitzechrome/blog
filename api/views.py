from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config
from django.db.models import Q

"""
Note :-

Please enter sender email and and secretkey in .env file 

>>>> Only the login register will not require the token, another all APIs must be required token

User can update delete and retrive  only his/her data.

User can update delete only his/her post.

"""

class Register(APIView):

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            if user:
                json = {
                    'user': f' User registered Successfully...',
                    'status': status.HTTP_201_CREATED,
                }
            return Response(json)
        else:
            json = {
                'message': 'registration fail....',
                'status': 400,
            }
            return Response(json)

class Login(viewsets.ViewSet):

    def create(self, request):
        username = request.data.get('Username', None)
        password = request.data.get('Password', None)

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            json = {
                'user': f'{username} login Successfully...',
                'token':str(token),
                "statu":status.HTTP_200_OK
            }
            return Response(json)
        else:
            return Response({'message': "Please enter valide Id Password","status":status.HTTP_404_NOT_FOUND})

# def sendemail(self,data):
#     contex={
#         "Title":data.title,
#         "Body":data.body,
#         "Author":data.auther.username
#     }
#     html_page = render_to_string("post.html", contex)
#     text_contant = strip_tags(html_page)
#     fail_silently = True
#     from_email = 'romit.zechrom@gmail.com'
#     to = data.auther.email
#     msg = EmailMultiAlternatives("Post creation", text_contant, from_email, [to])
#     msg.attach_alternative(html_page, "text/html")
#     try:
#         msg.send()
#     except Exception as ex:
#         print("not success",ex)

class PostListCreateView(generics.ListCreateAPIView):   
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def list(self, request):
        try:
            post = BlogPOST.objects.all().order_by('ID')
            data = []
            for i in post:
                data.append({
                    "ID": i.ID,
                    "title": i.title,
                    "body": i.body,
                    "auther": i.auther.username,
                })
            json_response = {"posts": data, "status": status.HTTP_200_OK}
            return Response(json_response)
        except Exception as ex:
            json_response = {"error": str(ex), "status":400}
            return Response(json_response)

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)       
            # sendemail(self,serializer.instance)
            print("hello")
            return Response({"message": "Create Sucessfully post.", "status":201})  
        except Exception as ex:
            json_response = {"error": str(ex), "status":400}
            return Response(json_response)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPOST.objects.all()

    def update(self, request, *args, **kwargs):

        try:
            partial = kwargs.pop('partial', False)
            try:
                instance = BlogPOST.objects.get(auther =self.request.user.id,ID = kwargs['pk'])
            except:
                return Response({"message":"You havere not Authority to update post","Success":400})

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"data":serializer.data, "status":200})

        except Exception as ex:
            json_response = {"error": str(ex), "status":400}
            return Response(json_response)

    def destroy(self, request, *args, **kwargs):
        try:
            try:
                instance = BlogPOST.objects.get(auther =self.request.user.id,ID = kwargs['pk'])
            except:
                return Response({"message":"You havere not Authority to update post","Success":400})
            
            self.perform_destroy(instance)
            return Response({"message": "Successfully post deleted.","status":204})    
        except Exception as ex:
            json_response = {"error": str(ex), "status":400}
            return Response(json_response)
        
