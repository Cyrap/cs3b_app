from datetime import datetime

""" Хэрэглээний функцууд """

def filter_queryset(request, queryset, params=None):
    """parametr-ээр дамжуулсан filter хийхэд ашиглагдах функц"""

    if params:
        for param in params:
            model_class = param["model"]
            filter_id = request.query_params.get(param["param"])

            if filter_id:
                types_list = model_class.objects.filter(id=filter_id).values_list(
                    "keywords", flat=True
                )
                queryset = queryset.filter(keywords__in=types_list)

    return queryset


def null_to_none(datas):
    """Convert 'null' string values to None"""

    mutable_data = datas.copy()
    for key, value in mutable_data.items():
        if isinstance(value, str) and value == "null":
            mutable_data[key] = None
    return mutable_data


def remove_key_from_dict(input_dict, keys):
    """Dict-ээс key ашиглаж д ата устгах"""

    if isinstance(keys, list):
        for key in keys:
            del input_dict[key]
    else:
        del input_dict[keys]

    return input_dict


def format_date(date_string, date_status=True):
    date = datetime.fromisoformat(date_string)

    year = date.year
    month = date.month
    day = date.day
    hours = str(date.hour).zfill(2)
    minutes = str(date.minute).zfill(2)

    if date_status:
        return f"{year} оны {month} сарын {day} - {hours}:{minutes}"
    else:
        return f"{year} оны {month} сарын {day}"
