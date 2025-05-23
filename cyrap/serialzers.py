from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Book, UserInfo, LendingRecord

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserInfo
        fields = '__all__'

class LendingRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = LendingRecord
        fields = '__all__'
    
    def get_user(self, obj):
        return "f{obj.user.username}"