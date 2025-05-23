def get_status_display(self, obj):
    if hasattr(obj, 'get_status_display'):
        return obj.get_status_display()
    return None


def get_status_name(self, obj):
    return obj.source.name if obj.source else None