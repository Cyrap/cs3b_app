from .serialzers import BookSerializer, LendingRecordSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, Category, LendingRecord
from main.utils.api import api_delete, api_get, api_post, api_put
from main.utils.generic_serializer import create_serializer

class BookApiView(generics.GenericAPIView):
    queryset = Book.objects.all().order_by("-id")
    serializer_class = BookSerializer
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAuthenticated()]

    def get(self, request, pk=None):
        queryset = self.get_queryset()

        category_filter = request.query_params.get("category")
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)

        search_query = request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return api_get(queryset, self.get_serializer_class(), request, pk)


    def post(self, request):
        return api_post(self.get_serializer_class(), request)

    def put(self, request, pk):
        return api_put(self.get_queryset(), self.get_serializer_class(), request, pk)

    def delete(self, request, pk):
        return api_delete(self.get_queryset(), pk)


class CategoryApiView(generics.GenericAPIView):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = create_serializer(Category)
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAuthenticated()]

    def get(self, request, pk=None):
        return api_get(self.get_queryset(), self.get_serializer_class(), request, pk)

    def post(self, request):
        return api_post(self.get_serializer_class(), request)

    def put(self, request, pk):
        return api_put(self.get_queryset(), self.get_serializer_class(), request, pk)

    def delete(self, request, pk):
        return api_delete(self.get_queryset(), pk)


class LendingRecordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LendingRecord.objects.all().order_by("-start_date")
    serializer_class = LendingRecordSerializer

    def get(self, request, pk=None):
        queryset = self.get_queryset()

        queryset = queryset.filter(user=request.user)

        return api_get(queryset, self.get_serializer_class(), request, pk)

    def post(self, request):
        return api_post(self.get_serializer_class(), request)

    def put(self, request, pk):
        return api_put(self.get_queryset(), self.get_serializer_class(), request, pk)

    def delete(self, request, pk):
        return api_delete(self.get_queryset(), pk)