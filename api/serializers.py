from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ['author', 'post']


class FollowSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username',
    #                                     default=serializers.CurrentUserDefault())
    # following = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        fields = ('user', 'following')
        model = Follow
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=('user', 'following'),
        #         message='You have already followed this account.'
        #     )
        # ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', )
        model = Group

