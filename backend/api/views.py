from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,parser_classes
from .serializers import TaskSerializer,UserSerializer,PostSerializer,FollowerSerializer
from .models import *
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions,generics
from rest_framework.parsers import MultiPartParser, FormParser
from chat.serializers import CompleteUserSerializer
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.inspectors import SerializerInspector
from  . import swagger_helper
from rest_framework.views import APIView


# Create your views here.

@api_view(['GET'])
def hello(request:Request):

    return Response(
        {"message":"hello world"},status=status.HTTP_200_OK)



@swagger_auto_schema(
        method="GET",
        responses={
            200:swagger_helper.post_serialized
        }
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def show_allposts(request:Request):
    serialized=PostSerializer(Post.objects.all(),many=True)
    return Response(serialized.data,status=status.HTTP_200_OK)



@swagger_auto_schema(
        method="POST",
        operation_description="create a post",
        manual_parameters=[
            openapi.Parameter(
            "title",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=True
            ),
            openapi.Parameter(
            "description",
            openapi.IN_QUERY,
            description="description",
            type=openapi.TYPE_STRING,
            required=True
            ),
            
            openapi.Parameter(
            "content",
            openapi.IN_FORM,
            description="the file of the post in a proper form",
            type=openapi.TYPE_STRING,
            required=True
            ),
            
        ],


)

@api_view(['POST','PUT'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_post(request:Request):

    print(request.data)
    post=PostSerializer(data=request.data,many=False)
   
    if post.is_valid():
        post.save(author=request.user)
        
        return Response({
        "ok":True,
        },status=status.HTTP_200_OK)
    else:
        print(post.errors)
        return  Response("Error", status=status.HTTP_503_SERVICE_UNAVAILABLE)
    

@swagger_auto_schema(
        method="POST",
        operation_description="to pass serailized user by username given",
        manual_parameters=[
            openapi.Parameter(
            "username",
            openapi.IN_QUERY,
            description="username",
            type=openapi.TYPE_STRING,
            required=True


            )
        ],
        responses={
            200:swagger_helper.user_serialized
        }
)

@api_view(['POST'])
def getUserByUsername(request:Request):
    username = request.data['username']
    user= User.objects.get(username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data,status=status.HTTP_200_OK)


class getAllCompletedUsers(generics.ListAPIView):
    serializer_class=CompleteUserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)
    
    def get_serializer_context(self):
        context= super().get_serializer_context()
        context['request']=self.request
        return context



# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def filter_users(request:Request):
#     key=request.data["key"]
#     users=User.objects.filter(username__contains=key)
#     serialized=CompleteUserSerializer(users,many=True)
#     return Response(serialized.data,status=status.HTTP_200_OK)
    

class filterCompletedUsers(generics.ListAPIView):
    serializer_class=CompleteUserSerializer
    permission_classes=[permissions.IsAuthenticated]

    # def get_queryset(self):
    #     key=self.request.query_params.get("key")
    #     return User.objects.filter(username__contains=key)
    
    def post(self,request,*args,**kwargs):
        key = request.data.get("key")
        queryset = User.objects.filter(username__contains=key).exclude(id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def get_serializer_context(self):
        context= super().get_serializer_context()
        context['request']=self.request
        return context



@swagger_auto_schema(
        method="post",
        manual_parameters=[
            openapi.Parameter(
                "following_id",
                openapi.IN_QUERY,
                description="Following user id",
                type=openapi.TYPE_INTEGER, 
                required=True
            )
        ],
        responses={
            201:swagger_helper.follower_serialized
        }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_following(request:Request):
    followed_id=request.data["following_id"]
    follower=request.user
    followed=User.objects.get(pk=followed_id)
    followerObj=Follower.objects.create(follower=follower,followed=followed)
    serialized=FollowerSerializer(followerObj,many=False)
    return Response(serialized.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_followers(request:Request):
    pass

@api_view(['GET'])
def get_followings(request:Request):
    pass


@swagger_auto_schema(
        method="post",
        manual_parameters=[
            openapi.Parameter(
            "following_id",
            openapi.IN_QUERY,
            description="id of the user you want to remove from your follower list",
            type=openapi.TYPE_INTEGER,
            )

        ],
)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_follower(request:Request):
    id=request.data['following_id']
    followed=User.objects.get(pk=id)
    followerObj=Follower.objects.get(follower=request.user,followed=followed)
    followerObj.delete()
    response={
        "message":f"user with username:{followed.username} unfollowed by {request.user.username}"
    }
    return Response(data=response,status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_complete_user(request:Request):
    user=request.user
    serialized=CompleteUserSerializer(user,many=False)
    return Response(data=serialized.data,status=status.HTTP_200_OK)






class PostAPIView(APIView):

    permission_classes=[permissions.IsAuthenticated]
    @swagger_auto_schema(
    # method="get",
    operation_description="get user posts",
    
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="your jwt access token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="A list of loggedin-user posts",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                        title="user posts",
                        type=openapi.TYPE_OBJECT,
                        properties={field_name: openapi.Schema(type=field_instance.__class__.__name__)
                                    for field_name, field_instance in PostSerializer().get_fields().items()}
                    )
            )
        ),
    }
)

    def get(self,request:Request):
        posts= Post.objects.filter(author=request.user)
        serialized=PostSerializer(posts, many=True)
        return Response(serialized.data,status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
            operation_description="get posts by author username",
            manual_parameters=[
                openapi.Parameter(
                    "username",
                    openapi.IN_QUERY,
                    description="the author username",
                    type=openapi.TYPE_STRING   
                )
            ],
            responses={
                200:swagger_helper.post_serialized
            }
    )
    
    def post(self,request:Request):
        # data=request.data
        username=request.data["username"]
        posts=Post.objects.filter(author__username=username)
        serialized=PostSerializer(posts,many=True)
        return Response(data=serialized.data,status=status.HTTP_200_OK)
    

    

@swagger_auto_schema(
        method="POST",
        operation_description="add user to a post liked_by field",
        manual_parameters=[
            swagger_helper.authorization_param,
            openapi.Parameter(
                name="post_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200:swagger_helper.post_serialized,
            404:"not found"
        }
)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_post(request:Request):
    user=request.user
    post_id=request.data["post_id"]
    try:
        post=Post.objects.get(id=post_id)
        post.liked_by.add(user)
        serialized=PostSerializer(post,many=False)
        return Response(serialized.data,status=status.HTTP_200_OK)
    except:
        return Response({"error":"post not found"},status=status.HTTP_404_NOT_FOUND)
    


# class PostListView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({"request": self.request})
#         return context

@swagger_auto_schema(
        method="POST",
        operation_description="return is_liked=true if the user liked the post and reverse",
        manual_parameters=[
            swagger_helper.authorization_param,
            openapi.Parameter(
                name="post_id",
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                required=True
            )
        ],
        responses={
            200:"is_liked=true/false",404:"not found"
        }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def is_liked_by_user(request:Request):
    user=request.user
    post_id=request.data["post_id"]
    try:
        post=Post.objects.get(id=post_id)
        if user in post.liked_by.all():
            return Response({"is_liked":True},status=status.HTTP_200_OK)
        else:
            return Response({"is_liked":False},status=status.HTTP_200_OK)
    except:
        return Response({"error":"post not found"},status=status.HTTP_404_NOT_FOUND)
    

@swagger_auto_schema(
        method="post",
        operation_description="dislike a post",
        manual_parameters=[
            swagger_helper.authorization_param,
            openapi.Parameter(
                name="post_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200:swagger_helper.post_serialized,
            204:"post doesn't exist",
            401:"unauthorized"
        }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def dislike_post(request:Request):
    post_id=request.data['post_id']
    try:
        post=Post.objects.get(id=post_id)
        post.liked_by.remove(request.user)
        serialized=PostSerializer(post,many=False)
        return Response(serialized.data,status=status.HTTP_200_OK)
    except:
        return Response(data={"error":f"post with id {post_id} doesn't exist"},status=status.HTTP_204_NO_CONTENT)





    





