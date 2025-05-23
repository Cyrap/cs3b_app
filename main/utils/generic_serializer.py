from rest_framework import serializers


def create_serializer(model_class, model_fields='__all__'):

    class GenericModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = model_fields

    return GenericModelSerializer


def create_method_serializer(model_class, model_fields='__all__', method_fields=None):

    method_fields = method_fields or {}

    meta_attrs = {'model': model_class, 'fields': model_fields}
    Meta = type('Meta', (object,), meta_attrs)

    serializer_attrs = {'Meta': Meta}

    for field_name, method in method_fields.items():
        serializer_attrs[field_name] = serializers.SerializerMethodField()

        serializer_attrs[f'get_{field_name}'] = method

    GenericModelSerializer = type(
        'GenericModelSerializer',
        (serializers.ModelSerializer,),
        serializer_attrs
    )

    return GenericModelSerializer