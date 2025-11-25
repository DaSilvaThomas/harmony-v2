from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplie value par arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def divide(value, arg):
    """Divise value par arg"""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Récupère un item dans un dictionnaire"""
    return dictionary.get(key)