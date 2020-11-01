from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()

from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password")


class LessonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class LessonUserSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLog
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['user_id'] = LessonUserSerializerMini(many=False,
                                                          read_only=True)
        self.fields['lesson_id'] = LessonSerializer(many=False, read_only=True)

        return super(LessonLogSerializer, self).to_representation(instance)
