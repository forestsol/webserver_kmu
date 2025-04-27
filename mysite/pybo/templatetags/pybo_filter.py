from django import template

register = template.Library()

@register.filter  # 애너테이션
def sub(value, arg):
    return value - arg