from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from django.db.models import Q
from main.utils.functions import null_to_none
from rest_framework.pagination import PageNumberPagination
from django.core.files.uploadedfile import UploadedFile
from django.db import models


def handle_response(data, message=None, status_code=status.HTTP_200_OK):
    response = {"message": message} if message else {}
    response["data"] = data
    return Response(response, status=status_code)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'current_page'

def api_get(queryset: QuerySet, serializer_class: type[Serializer], request: Request, pk: int = None, data=None, search_fields=None, is_paginated=False):
    chosen_field = request.GET.get('chosen_field','')
    chosen_field_value = request.GET.get('chosen_filter','')

    if chosen_field:
        if chosen_field_value != '' and chosen_field_value != 'undefined':
            queryset = queryset.filter(**{chosen_field: chosen_field_value})

    if search_fields:
        search_value = request.GET.get('search', '')
        if search_value:
            query = Q()
            for field in search_fields:
                query |= Q(**{f"{field}__icontains": search_value})
            queryset = queryset.filter(query)

    if pk:
        instance = get_object_or_404(queryset, pk=pk)
        serializer = serializer_class(instance)
        if data:
            serializer = serializer_class(data, many=True)
        return handle_response(serializer.data)

    if is_paginated:
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = serializer_class(page, many=True)

            page_size = int(request.query_params.get(paginator.page_size_query_param, paginator.page_size))
            total_items = paginator.page.paginator.count
            total_pages = (total_items // page_size) + (1 if total_items % page_size != 0 else 0)

            paginated_response = paginator.get_paginated_response(serializer.data)
            paginated_response.data['total_pages'] = total_pages
            return paginated_response

    serializer = serializer_class(queryset, many=True)
    if data:
        return handle_response(data)

    return handle_response(serializer.data)

def api_post(serializer_class: type[Serializer], request: Request, data=None):
    try:
        serializer = serializer_class(data=null_to_none(request.data))
        if data:
            serializer = serializer_class(data=null_to_none(data))
        if serializer.is_valid():
            serializer.save()
            return handle_response(serializer.data, "Амжилттай үүсгэлээ", status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return handle_response(serializer.errors, "Системд алдаа гарлаа!", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)


def api_put(queryset: QuerySet, serializer_class: type[Serializer], request: Request, pk: int, data=None):
    try:
        instance = get_object_or_404(queryset, pk=pk)

        data = request.data if data is None else data

        data = data.copy()

        for field in instance._meta.fields:
            if isinstance(field, models.FileField):
                field_name = field.name
                if field_name in data and not data.get(field_name):
                    data[field_name] = None
                elif field_name not in data or not isinstance(data.get(field_name), UploadedFile):
                    data[field_name] = getattr(instance, field_name)

        serializer = serializer_class(instance, data=null_to_none(data), partial=True)
        if serializer.is_valid():
            serializer.save()
            return handle_response(serializer.data, "Амжилттай заслаа")
        else:
            print(serializer.errors)
            return handle_response(serializer.errors, "Системд алдаа гарлаа!", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return handle_response({"error": str(e)}, "Системд алдаа гарлаа!", status.HTTP_500_INTERNAL_SERVER_ERROR)



def api_delete(queryset: QuerySet, pk: int):
    instance = get_object_or_404(queryset, pk=pk)
    instance.delete()
    return handle_response({}, "Амжилттай устгалаа", status.HTTP_204_NO_CONTENT)
