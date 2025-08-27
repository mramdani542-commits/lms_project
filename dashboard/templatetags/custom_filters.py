from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Memungkinkan akses dictionary dengan variabel sebagai key di dalam template Django.
    Contoh: {{ my_dict|get_item:my_variable }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
