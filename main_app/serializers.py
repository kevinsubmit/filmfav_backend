from rest_framework import serializers
from django.contrib.auth.models import User # add this line to list of imports

from .models import   Review,Comment

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username',  'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
        #   email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user
  
class ReviewSerializer(serializers.ModelSerializer):
   class Meta:
      model = Review
      fields = ['id','user','movie','text','rating','created_at']
      read_only_fields = ['user']  # 将 user 字段标记为只读
   def create(self, validated_data):
        # 获取当前请求的用户
      user = self.context['request'].user  # 通过上下文获取当前用户
      validated_data['user'] = user
      return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = ['id','user','review','text','created_at']