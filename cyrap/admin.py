from django.contrib import admin
from .models import Book, Category, LendingRecord, UserInfo

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(LendingRecord)
admin.site.register(UserInfo)