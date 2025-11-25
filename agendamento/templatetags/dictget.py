from django import template
register = template.Library()

@register.filter
def dictget(d, key):
    try:
        return d.get(key, "")
    except:
        return ""
