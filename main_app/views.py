

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions # modify these imports to match
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Review,Comment
from django.shortcuts import get_object_or_404


from .serializers import UserSerializer,ReviewSerializer,CommentSerializer

# Create your views here.
class Home(APIView):
    def get(self,request):
        message = {'mes':'weclome'}
        return Response(message)

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
  

  # Review API
class ReviewListCreateAPIView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  # get all reviews
  def get(self,request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews,many=True)
    return Response(serializer.data)
  
  # create the review
  def post(self,request):
    serializer = ReviewSerializer(data=request.data,context={'request': request})
    if serializer.is_valid():
       serializer.save()  # 不需要传递任何参数,自动将 user 添加到 validated_data 中并保存
       return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# single Review （get、update、delete）
class ReviewDetailAPIView(APIView):
    permission_classes =  [permissions.IsAuthenticated]

    # 获取单个评论的详细信息 get the signle review's detail
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Comment API (get、update、delete）
class CommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

     # 获取某个评论下的所有评论  get one specfiec review's all comments
    def get(self, request, review_id):
        comments = Comment.objects.filter(review__id=review_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
     # 创建某个评论下的单条评论 create one specfiec review's one comment
    def post(self, request, review_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review_id=review_id)  # 将评论与评论和当前用户关联  connect review with presnet user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 单个 Comment 视图（获取、删除） get the signle Comment's detail
class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)