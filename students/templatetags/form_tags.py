from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def average(queryset, field_name):
    """
    Compute the average of a numeric field in a queryset.
    Example: {% with enrollments|average:"exam_score" as avg %}
    """
    values = [getattr(obj, field_name) for obj in queryset if getattr(obj, field_name) is not None]
    if not values:
        return 0
    return sum(values) / len(values)

@register.filter
def get_field(queryset, field_name):
    """
    Get a list of values for a field.
    Example: {% for val in enrollments|get_field:"course_code" %}
    """
    return [getattr(obj, field_name) for obj in queryset]
