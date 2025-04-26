from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """Adds CSS classes to form field widgets"""
    return value.as_widget(attrs={'class': f"form-control {css_class}"})